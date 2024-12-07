import streamlit as st
import pandas as pd
import os
import requests
from price_checker import monitor_prices  # Import the monitor_prices function from the price checker file

#this file contains crucial elements that will be part of the TRACKED COINS PAGE on the app. 
#First, it circles back to some functions already handled in the price_checker.py file (more precisely,
#it defines analogous functions in certain situations). After that, a function that will save the user's
#preferred way of receiving notifications is defined. We then implement another function that contains
#all necessary elements that will be displayed in the app's tracked coins page (more detailed comments will
#follow directly nearby the function).

# Paths for saving tracked coins and user preferences
TRACKED_COINS_FILE = "tracked_coins.csv"
NOTIFICATION_PREF_FILE = "notification_preferences.csv"

#we start by defining a function that will fetch the symbols that are appropriate for the Binance API
def fetch_binance_symbols():
    """
    Fetches the list of supported symbols from Binance API.
    Returns a list of valid coin symbols.
    """
    try:
        response = requests.get("https://api.binance.com/api/v3/exchangeInfo")
        response.raise_for_status() #helps to handle HTTP errors
        data = response.json() #formatting with json
        symbols = [symbol["symbol"][:-4] for symbol in data["symbols"] if symbol["symbol"].endswith("USDT")]
        return list(set(symbols))
    except Exception: #unless there's an exception, i.e. mistake, the code after 'try...' is executed
        st.error("Failed to fetch Binance symbols. Please try again later.") #in this case, we raise a streamlit error in case an exception is encountered
        return [] #if exception happens, the returned list is empty

#when defining the symbols variable, we use '.endswith' because we only want symbols that entail a processed 
# pair in a form analogous to, for example,'BTCUSDT' (we do not want any other ending that differs from 'USDT')
#however, we then do not want USDT to remain visible in the symbol of the coin. This is why we use 
#slicing ('[:-4]') to remove the last 4 characters of all the strings. Coming back to the previous example,
#slicing would let us go from 'BTCUSDT' to 'BTC'



#using a logic which is very similar to the one used in the price_checker.py file, we define functions that allow us to load and then
#save the data from the specific files containing respectively the tracked coins and the user's notification preferences
#however, this time we use if instaed of if not, meaning that the structure will appear, so to say, in the opposite way
def load_tracked_coins():
    """The data of the tracked coins is loaded from the tracked coins file."""
    if os.path.exists(TRACKED_COINS_FILE): #we use the os module to check that the 'tracked_coins.csv' file exists
        return pd.read_csv(TRACKED_COINS_FILE) #if the file does exist, we return a dataframe thanks to the pd.read_csv function
    else:
        return pd.DataFrame(columns=["coin", "threshold"]) #if the file doesn't exist, we return an empty dataframe with the specified columns

def save_tracked_coins(data):
    """Save the tracked coins data to the file."""
    data.to_csv(TRACKED_COINS_FILE, index=False)
    #after having manipulated the data of the tracked coins in a dataframe structure with the 
    # 'load_tracked_coins' function, we save the mentioned data back into the csv files thanks to 
    # the '.to_csv' function (additionally, we set the index=False because we do not want to keep the indexes).
    # As a brief reminder, the tracked coins are correlated to the user's choice.


def get_user_notification_preferences():
    """Load the user's notification preferences."""
    if os.path.exists(NOTIFICATION_PREF_FILE): #following the same reasoning as the 'load_tracked_coins' function, it first checks the existence of the 'notification_preference.csv' file
        return pd.read_csv(NOTIFICATION_PREF_FILE).iloc[0] #we assume that the dataframe only has one row, and thus locate it thanks to '.iloc[0]'
    else:
        return {"email": ""} #return an empty dictionary if the user did not insert any email for the notification preference

def save_notification_preferences(email):
    """Save the user's notification preferences."""
    pd.DataFrame([{"email": email}]).to_csv(NOTIFICATION_PREF_FILE, index=False)
#this function will save the user's notification preference in the appropriate csv file. 
#before creating the csv file, we create a dataframe with key "email" and the specific email chosen by the user as value
#the dataframe will have one row and two columns


#the following function contains the necessary elements that will allow to display the TRACKED COINS PAGE
def show_tracked_coins_page():
    """
    Displays the Tracked Coins page.
    Allows users to manage tracked coins and update notification preferences.
    """
    #OBSERVATION: as applicable in other parts of the code, we asked ChatGPT a comprehensive explanation
    #on how to use 'st.session_state'
    # We load tracked coins and ensure it's always synced with the CSV file
    if "tracked_coins" not in st.session_state or st.session_state.get("force_refresh", False): #we check the force refresh mechanism; in brief, force refresh is used to induce manual reloadings of data
        st.session_state["tracked_coins"] = load_tracked_coins()
        st.session_state["force_refresh"] = False  # Reset the refresh flag
        #OBSERVATION: in order to be able to come up with the above lines of code that use "force refresh", 
        #we specifically asked ChatGPT to explain how we could approach a force refresh;
        #we then cam up with our own code (which adopted a quite different approach), and then asked again if our code was clear/did what we wanted it to do
    

    st.title("Tracked Coins & Notifications") #setting the title

    # Fetch Binance-supported symbols
    if "binance_symbols" not in st.session_state:
        st.session_state["binance_symbols"] = fetch_binance_symbols()

    # Load tracked coins
    tracked_coins = st.session_state["tracked_coins"].copy()  # We make a copy in order to detect changes
    #by making a copy, changes that are not saved will have no impact until they are actually saved

    # Load user notification preferences using the previously defined function
    preferences = get_user_notification_preferences()
    email = preferences.get("email", "") #we want to indeed get the value that corresponds to the key "email", i.e. this value will be the inserted email address 

    # Section 1: Tracked Coins
    st.subheader("Tracked Coins")

    # Persistent success message display: we check if there's an existent success message in session state
    #if that is the case, the message is displayed and then cleared
    if "success_message" in st.session_state and st.session_state["success_message"]:
        st.success(st.session_state["success_message"])
        st.session_state["success_message"] = None  # Clear the message after displaying

    changes_made = False  # We track if any changes are made

    #OBSERVATION:  for the lines below, we asked ChatGPT to help us to conceptualize some code that allows 
    #a user to update a threshold for tracked coins and for removing them from the tracked list. 
    #The first insights were more basic than what we wanted to implement, 
    #so we further developed the code using ChatGPT as support (specifically by asking it 
    #target questions about aspects that we wanted to have in our function, such as having three columns of 
    #which one contained written text, one a number input field, and the last a button that removed the coin 
    #from the tracked coins dataframe
    if not tracked_coins.empty:
        for index, row in tracked_coins.iterrows():
            col1, col2, col3 = st.columns([6, 3, 1]) #the numbers in the parentheses track how many units of space will be occupied by each column
            col1.write(f"**{row['coin']}** (Threshold: {row['threshold']}%, Initial Price: {row.get('initial_price', 'N/A')})")
            new_threshold = col2.number_input(
                f"Set new threshold for {row['coin']}",
                min_value=0.1,  # Prevent user from entering 0
                value=row["threshold"],
                key=f"threshold_{index}",
            )
            if new_threshold != row["threshold"]:
                tracked_coins.at[index, "threshold"] = new_threshold
                changes_made = True
            if col3.button("❌ Remove", key=f"remove_{index}"):
                # Remove the coin from the DataFrame
                tracked_coins = tracked_coins.drop(index)
                save_tracked_coins(tracked_coins)

                # Set a flag to reload tracked coins
                st.session_state["force_refresh"] = True

                # Show a success message and refresh the page
                st.session_state["success_message"] = f"{row['coin']} removed from the tracking list."
                st.rerun()

    else:
        st.info("No coins are currently being tracked.") #if the 'tracked_coins' are empty, we display this informational message

    # Add an "Apply Changes" button
    apply_button = st.button("Apply Changes")

    if apply_button:
        # Check if the dataframe has been modified, here, too, we asked ChatGPT for inspiration, however
        #the insight we got provided us with basic knowledge but didn't satisfy the goal we had in mind
        #so we further developed this feature, spatiating from the insights we got (which were indeed a 
        #mere inspiration)
        if changes_made:
            save_tracked_coins(tracked_coins) #we call the previously defined function
            st.session_state["tracked_coins"] = tracked_coins
            st.session_state["tracked_coins_message"] = ("success", "Changes applied successfully!")
            st.rerun()  # Refresh the page
        else:
            st.session_state["tracked_coins_message"] = ("info", "No changes were made.")
            st.rerun()  # Refresh the page

    # Display the specific message below the button
    if "tracked_coins_message" in st.session_state:
        message_type, message_text = st.session_state["tracked_coins_message"]
        if message_type == "success": #message defined if 'changes_made'
            st.success(message_text)
        elif message_type == "info": #message defined in other situations (i.e., else)
            st.info(message_text)
        # We clear the message after displaying it
        del st.session_state["tracked_coins_message"]

    # Let the user add new coin to track
    st.subheader("Add a Coin to Track")
    new_coin = st.text_input("Enter coin symbol (e.g., BTC, ETH):").strip().upper() #.strip() removes any white spaces at the beginning/end of the string; .upper() gives us the string with all uppercases
    new_threshold = st.number_input("Enter threshold (%)", min_value=0.1, step=0.1, value=1.0)  # Prevent 0 from being input by the user
    if st.button("Add Coin to Track"):
        if not new_coin: #this signals the user to enter a valid coin symbol in case they push the button but have not put any coin in the text input case
            st.error("Please enter a valid coin symbol.")
        elif new_coin not in st.session_state["binance_symbols"]: #prevent the user from entering a coin with a symbol not supported by Binance
            st.error(f"{new_coin} is not a valid Binance-supported symbol.")
        elif new_coin in tracked_coins["coin"].values: #to signal the user that the coin they are trying to input is already in the tracked ones
            st.warning(f"{new_coin} is already being tracked.")
        else:
            # Fetch the current price of the coin to set as initial price (indeed, provided that none of the above parts of the if clause apply)
            initial_price = requests.get(
                f"https://api.binance.com/api/v3/ticker/price", params={"symbol": f"{new_coin}USDT"}
            ).json().get("price", None) #.get("price", None) gives us the value associated with the "price" key; if that value is not present, 'None' is given instaed

            if initial_price is None:
                st.error(f"Failed to fetch current price for {new_coin}. Try again later.")
            else: #i.e., if we get the initial price successfully
                initial_price = float(initial_price)
                new_row = pd.DataFrame({
                    "coin": [new_coin],
                    "threshold": [new_threshold],
                    "initial_price": [initial_price],
                }) #we created a new dataframe with the data related to the newly input coin, the new threshold, and the coin's initial price
                tracked_coins = pd.concat([tracked_coins, new_row], ignore_index=True) #we concatenate the existing 'tracked_coins' dataframe and 'new_row' dataframe by appending rows
                save_tracked_coins(tracked_coins) #call the previously defined function to, again, save to the tracked coins
                st.session_state["tracked_coins"] = tracked_coins #snychronizing updated tracked coins with session state
                st.session_state["success_message"] = (
                    f"{new_coin} has been added to the tracked coins list with an initial price of {initial_price:.2f}."
                )
                st.rerun()

    # Section 2: Notification Preferences
    st.subheader("Notification Preferences")
    st.write("Set how you would like to be notified when thresholds are met.")

    #input case where the user will add the email address to which the notifications must be sent
    updated_email = st.text_input("Email Address", value=email, placeholder="Enter your email address")

    if st.button("Update Preferences", key="update_preferences"):
        if not updated_email: #we remind the user to provide an email
            st.error("Please provide your email address.")
        else:
            save_notification_preferences(updated_email) #call the previously defined function
            st.session_state["notification_success_message"] = "Notification preferences updated successfully!"
            st.rerun()

    if "notification_success_message" in st.session_state:
        st.success(st.session_state["notification_success_message"])
        del st.session_state["notification_success_message"] #after it has been displayed, we delete the notification success message

    st.markdown("---")
    st.caption("You will be notified when a tracked coin crosses the specified threshold.")

        # Section 3: Manual Price Check Trigger
    st.subheader("Manual Price Check")
    if st.button("Run Price Check Now"):
        try:
            # Run the price checker, specifically by using the 'monitor_prices' function defined in the file 'price_checker.py'
            monitor_prices()
            # We reload the tracked coins from the CSV file after price check; again, we use the previously defined function
            st.session_state["tracked_coins"] = load_tracked_coins()
            # Finally, we set a success message to display after the price check
            st.session_state["price_check_success_message"] = (
                "Price check completed! Notifications sent where thresholds were met. List updated."
            )
            st.rerun()  # Refresh the page to reflect updates (analogosuly to other instances where we use 'st.rerun')
        except Exception as e:
            # We want to show error if price checking fails
            st.error(f"Error during price check: {e}") #we dynamically display the error directly using streamlit functionalities

    # Display the success message after running the price check
    if "price_check_success_message" in st.session_state:
        st.success(st.session_state["price_check_success_message"])
        del st.session_state["price_check_success_message"]  # We clear the message after displaying
