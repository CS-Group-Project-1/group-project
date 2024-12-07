import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
import requests
import os
from email_credentials import SMTP_EMAIL, SMTP_PASSWORD  # Import email credentials from the separate file 

#This file tackles the functionality that allows to send an email when the percentage threshold is met
#In extent, it loads (and then saves) the tracked coins and the preferences of the user for notification
#Then, it fetches the coin price, which will then be analyzed extensively through the 'monitor_prices()' 
# function, which also implements the mechanisms necessary to check whether the percentage thershold has been
# met and, if that is the case, to send an email notification to the user. The coins for which a notification
# has been sent are then removed from tracking.


#first, we define which files contain the data regarding tracked coins and the user's notification preferences
TRACKED_COINS_FILE = "tracked_coins.csv"
NOTIFICATION_PREF_FILE = "notification_preferences.csv"

#url that we will use to make a request to the API
API_URL = "https://api.binance.com/api/v3/ticker/price"

#to send the email, we need to state that we will use the gmail server
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

#defining the function that will send the email
def send_email(to_email, subject, body):
    """Send an email notification."""
    try:
        msg = MIMEMultipart()
        msg["From"] = SMTP_EMAIL
        msg["To"] = to_email
        msg["Subject"] = subject

        # Email body
        msg.attach(MIMEText(body, "plain"))

        # Connect to the email server and send the email; OBSERVATION: asked ChatGPT insights on how we could connect to the server and then send the email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.send_message(msg)

        print(f"Email sent to {to_email}")
    except Exception as e: #block of code after try is executed unless there's an exception, i.e. unless an error exists
        print(f"Failed to send email: {e}") #format string allows to dynamically see what the error is


def load_tracked_coins():
    """The data of the tracked coins is loaded from the tracked coins file."""
    if not os.path.exists(TRACKED_COINS_FILE): #we use the os module to check that the 'tracked_coins.csv' file exists
        return pd.DataFrame(columns=["coin", "threshold", "initial_price"]) #if the file doesn't exist, we return an empty dataframe with the specified columns
    return pd.read_csv(TRACKED_COINS_FILE) #if the file does exist, we return a dataframe thanks to the pd.read_csv function


def save_tracked_coins(data):
    """Saves the updated tracked coins data back to the file."""
    data.to_csv(TRACKED_COINS_FILE, index=False)
    #after having manipulated the data of the tracked coins in a dataframe structure with the 
    # 'load_tracked_coins' function, we save the mentioned data back into the csv files thanks to 
    # the '.to_csv' function (additionally, we set the index=False because we do not want to keep the indexes).
    # As a brief reminder, the tracked coins are correlated to the user's choice.
    


def get_user_notification_preferences():
    """Loads the user's notification preferences.""" 
    if not os.path.exists(NOTIFICATION_PREF_FILE): #following the same reasoning as the 'load_tracked_coins' function, it first checks the existence of the 'notification_preference.csv' file
        return {"email": ""} #if the file does not exist, we return an empty dictionary to avoid errors (reasoning behind the building of the dictionary: after the email key, the ' ""' empty value would represent the inserted email address if it existed)
    return pd.read_csv(NOTIFICATION_PREF_FILE).iloc[0].to_dict()
    # in this last line of the function, if the file does exist, we assume that the 'notification_preferences.csv'
    #file only contains data in one row (the data must indeed correspond to the "email" designation followed by the selected user email);
    #given this assumption, we are only interested in the first row, and we locate it thanks to .iloc[0].
    #Finally, we want the information in the dataframe which we got, as before, by applying 'pd.read_csv',
    # to be in a dictionary format (for convenience in relation to accessing the data); for this we use
    #.to_dict: this way, we make sure that we get a dictionary where the key is "email", and the value
    #is the user's email address


def fetch_coin_price(coin):
    """Fetches the current price of a coin from Binance API."""
    try:
        response = requests.get(API_URL, params={"symbol": f"{coin}USDT"}) #we make a GET request to the API
        response.raise_for_status() #helps to handle HTTP errors
        data = response.json() #we use json formatting for the response that we get from the API
        return float(data["price"]) #we want the price column of our data to be in float format; this is then needed in further calculations
    except Exception as e: #we execute the block of code after try unless an exception (i.e. unless an error exists)
        print(f"Failed to fetch price for {coin}: {e}") #format string that allows us to dynamically see the different coin and exception in question in a specific case
        return None


def monitor_prices():
    """Monitor prices and send notifications when thresholds are met."""
    tracked_coins = load_tracked_coins() #to get the tracked coins
    preferences = get_user_notification_preferences() #to get the email address

    if tracked_coins.empty: #if it's the case, we print that no coin is currently being tracked
        print("No coins are being tracked.")
        return

    if not preferences.get("email"): #analgosuly, here we inform that no email address was added
        print("No email address configured for notifications.")
        return

    print("Checking prices...")

    coins_to_remove = [] #we initialize a list of the coins that have surpassed the percentage threshold (which is the notification criteria); after the notification, the coins will be removed from tracking

    #OBSERVATION: for the following lines of code, we asked ChatGPT advice on how to proceed for our function since
    #we needed help to come up with the right approach; starting from the basic insights we got, we further
    #built and developed the function by adding crucial elements for our user case
    for _, row in tracked_coins.iterrows(): # we use '_' as a placeholder when iterating over the rows in 'tracked_coins' since we only want iterrows to return the row itself and not the index
        coin = row["coin"]
        threshold = row["threshold"]
        initial_price = row["initial_price"]

        price = fetch_coin_price(coin)
        if price is None:
            continue

        # We calculate the percentage change
        percentage_change = ((price - initial_price) / initial_price) * 100
        print(f"{coin}: Current price = {price}, Initial price = {initial_price}, Change = {percentage_change:.2f}%")

        if abs(percentage_change) >= threshold:
            direction = "increased" if percentage_change > 0 else "decreased"
            subject = f"Price Alert: {coin} has {direction} by {percentage_change:.2f}%"
            body = (
                f"The price of {coin} has {direction} by {percentage_change:.2f}%.\n"
                f"Initial price: {initial_price} USDT\n"
                f"Current price: {price} USDT\n"
                f"Threshold: {threshold}%"
            )
            send_email(preferences["email"], subject, body)

            # Mark the coin for removal after notification by adding it to the dedicated list
            coins_to_remove.append(coin)

    # We remove from the tracking list coins for which a notification was received 
    if coins_to_remove:
        tracked_coins = tracked_coins[~tracked_coins["coin"].isin(coins_to_remove)] #here we asked again ChatGPT how we could filter the 'tracked_coins' dataframe so that the function excludes rows where the coin is in the 'coins_to_remove' list. 
        save_tracked_coins(tracked_coins)
        print(f"Removed the following coins from the tracking list: {', '.join(coins_to_remove)}")

#we make sure that the monitor_prices() function is run when executed directly to guarantee its modularity
#in other words, we ensure that the code below is executed only if the script is run directly/as a main program
if __name__ == "__main__":
    monitor_prices()
