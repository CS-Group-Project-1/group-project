import requests
import pandas as pd
import plotly.graph_objects as go

#This file encompasses a variety of functions that we classified as utils, i.e. as 
#functions that allow us to complete a very specific task that is then useful for other 
# files/scripts.
#The detailled content of the present file is as follows:
# - a function that interacts with the Binance API in order to fetch the data about the
#   historical prices of coins;
# - a function that calculates the percentage change in the price of coins;
# - a function that allows us to create the candlestick graph for the coin in question
#   (to create the graph, we use the plotly library).


# Function to fetch historical price data from the Binance API
def fetch_historical_data(coin, interval):
    """
    Fetches historical price data for the specified coin and interval from Binance API.

    Parameters:
        coin (str): The cryptocurrency ticker (e.g., 'BTC', 'ETH').
        interval (str): The interval for candlestick data (e.g., '1m', '1h', '1d').

    Returns:
        DataFrame: A pandas DataFrame containing historical price data.
        None: If the API call fails or data is not available.
    """
    symbol = f"{coin}USDT"  # Format the trading pair for Binance (e.g., BTCUSDT)
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit=100"
    #additional observation about the symbol: we have the symbol of the specific coin (which in the 
    #short example of the previous line is BTC) which is followed by the currency, which is consistently
    # USDT

    try:
        # Make the API request
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP issues
        data = response.json()

        # Convert the JSON data into a pandas DataFrame
        df = pd.DataFrame(data, columns=[
            "timestamp", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "trades", 
            "taker_buy_base", "taker_buy_quote", "ignore"
        ])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")  # Convert timestamps to readable format
        return df
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {coin}: {e}")
        return None
#in this and in several other instances, 'try...except...' allows us to handle possible situations where there 
#are mistakes in getting the data from the API

# Function to calculate percentage change over a time period
def calculate_percentage_change(df):
    """
    Calculates the percentage change in price from the first to the last data point.

    Parameters:
        df (DataFrame): A pandas DataFrame containing historical price data.

    Returns:
        float: The percentage change in price.
    """
    try:
        open_price = float(df.iloc[0]["open"])  # We want to get the opening price of the first row by using iloc (and we want to get it from the ["open"] column)
        close_price = float(df.iloc[-1]["close"])  # We get the closing price of the last row by using iloc (the reasoning is the same as in the previous line) 
        return ((close_price - open_price) / open_price) * 100  # Percentage change formula
    except Exception as e:
        print(f"Error calculating percentage change: {e}")
        return 0.0


# Function to plot a candlestick chart using Plotly
def plot_candlestick(df, coin, interval):
    """
    Plots a candlestick chart for the given DataFrame using Plotly.

    Parameters:
        df (DataFrame): A pandas DataFrame containing historical price data.
        coin (str): The cryptocurrency ticker (e.g., 'BTC', 'ETH').
        interval (str): The interval for candlestick data (e.g., '1h', '1d').
    """
    try:
        # We create a candlestick chart using Plotly
        fig = go.Figure(data=[go.Candlestick(
            x=df["timestamp"],  # X-axis: Timestamps
            open=df["open"].astype(float),  # Opening prices
            high=df["high"].astype(float),  # High prices
            low=df["low"].astype(float),  # Low prices
            close=df["close"].astype(float)  # Closing prices
        )])
        #in all the lines of code above, .astype() allows us to make sure that the data is in the correct
        #format, which in the present case is float


        # Now we update layout with titles and styling
        fig.update_layout(
            title=f"{coin} Candlestick Chart ({interval})",
            xaxis_title="Time",
            yaxis_title="Price (USDT)",
            xaxis_rangeslider_visible=False  # Hide the range slider for cleaner look
        )
        

        # Display the chart in Streamlit
        import streamlit as st # for convenience, we import streamlit here instaed of the beginning of the file
        st.plotly_chart(fig) #this allows us to display the chart in streamlit
    except Exception as e:
        print(f"Error creating candlestick chart: {e}")


# Function to send email notifications
# OBSERVATION: we asked ChatGPT for insights on the usage of smtplib and MIME modules to send emails notifications
# we got inspiration and  to some extent based ourselves on the received insights for the structure that
# can be used for the goal of sending notification with smtplib and MIME;
# we then critically adapted itthe insights to our specific case
def send_email_notification(coin, percentage_change, user_email):
    """
    Sends an email notification when the price threshold is met.

    Parameters:
        coin (str): The cryptocurrency ticker (e.g., 'BTC', 'ETH').
        percentage_change (float): The calculated percentage change.
        user_email (str): The recipient's email address.
    """
    try:
        import smtplib #common python library to send emails
        from email.mime.text import MIMEText 
        from email.mime.multipart import MIMEMultipart

        # We define the email sender and recipient
        sender_email = "your_email@gmail.com"  # This will need to be replaced with the own email 
        sender_password = "your_password"  # Analogously, this will need to be replaced with the own password 
        recipient_email = user_email

        # Email subject and body
        subject = f"Price Alert: {coin} has met your threshold!"
        body = f"The percentage change for {coin} is {percentage_change:.2f}%. Check Easy2Trade for more details."

        # Now we create the email
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = recipient_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        # Finally, we connect to the Gmail server and send the email
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()

        print("Email notification sent successfully!")
    except Exception as e:
        print(f"Error sending email notification: {e}")
