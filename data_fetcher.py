import os
import pandas as pd
import numpy as np
from binance.client import Client
from datetime import datetime, timedelta

#This file is geared towards fetching the historical data for the coins from the Binance API,
#like for example the price of the coins, the trading volume, and so on.
#The data is fetched for a predefined list of symbols, visible in the 'fetch_all_data' function.
#Another important thing implemented in this file is the processing of the fetched data
#in order to calculate volatility, average volume, and trend of the trades; these calculations
#are then saved into CSV files. Finally, the CSV files are further updated with the 
#categorization of volatility and average volume into categories (low, medium, high).


#Space for the Binance API credentials; since we access the historical data from the Binance API
# and we do not want our app to execute trades, we do not need an API KEY nor an API secret
#however, we still need to initialize the corresponding variables in order to be able to initialize binance client
API_KEY = ""
API_SECRET = ""

# Initialize Binance Client 
client = Client(API_KEY, API_SECRET)
#OBSERVATION: we asked ChatGPT to explain us how to initialize the Binance Client;
#we wanted to use Binance API client library (-->python-binance)
#in order to best interact with the API and be able to analyze aspects such as volatility 

# Directory to save data is created by using os 
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

#we define the function that fetches the historical data from the Binance API and saves it as a .csv file
#again, we reiterate that the name of the present function is similar to that of certain functions in some
#of our other scripts, and this is because of simplicity and convenience reasons
def fetch_historical_data(symbol, interval, lookback="1 year ago"):
    """
    Fetch historical data from Binance and save it as a CSV file.
    Includes volatility and average volume calculations.
    """
    try:
        # Fetch historical klines
        klines = client.get_historical_klines(symbol, interval, lookback) #OBSERVATION: we asked ChatGPT to tell us a method to fetch historical candlestick data and advice on how to convert the result to a dataframe

        # Convert to DataFrame
        df = pd.DataFrame(klines, columns=[
            "timestamp", "open", "high", "low", "close", "volume", "close_time",
            "quote_asset_volume", "number_of_trades", "taker_buy_base_asset_volume",
            "taker_buy_quote_asset_volume", "ignore"
        ])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df["close"] = df["close"].astype(float)
        df["volume"] = df["volume"].astype(float)

        # We calculate volatility (rolling standard deviation of % changes); 
        # OBSERVATION: we asked ChatGPT how we could approach this; the insigths given were useful,
        #we then took inspiration and adapted the code according to our needs
        df["volatility"] = df["close"].pct_change().rolling(window=7).std() * 100

        # Calculation of average volume (rolling mean); OBSERVATION: same approach as for volatility
        df["avg_volume"] = df["volume"].rolling(window=7).mean()

        # Add trend (Upward, Downward, Stable)
        # OBSERVATION: we asked ChatGPT how to use NumPy to identify 'Upward', 'Downward', or 'Stable'
        # trends in cryptocurrency price data; we then further developed the basic insights received to adapt them for our needs
        df["trend"] = np.where(df["close"].diff() > 0, "Upward",
                               np.where(df["close"].diff() < 0, "Downward", "Stable"))

        # Keep relevant columns
        df = df[["timestamp", "close", "volume", "volatility", "avg_volume", "trend"]]

        # Save to CSV; in particular, we save the data in CSV files with the name of the symbol
        #like for example 'BTCUSDT'
        save_path = f"{DATA_DIR}/{symbol}.csv"
        df.to_csv(save_path, index=False)
        print(f"Data for {symbol} saved to {save_path}")
    except Exception as e:
        print(f"Failed to fetch data for {symbol}: {e}")

#now we want to fetch the historical data for a predefined list of symbols, which we include in the function
def fetch_all_data():
    """
    Fetch historical data for a predefined list of symbols.
    """
    symbols = ["BTCUSDT", "ETHUSDT", "ADAUSDT", "SOLUSDT", "XRPUSDT", "MATICUSDT", "DOGEUSDT", "SHIBUSDT", "ARBUSDT", "OPUSDT", "AVAXUSDT", "ATOMUSDT", "DOTUSDT", "LINKUSDT", "LTCUSDT", "BNBUSDT", "UNIUSDT", "AAVEUSDT", "SANDUSDT", "MANAUSDT", "AXSUSDT", "FTMUSDT", "NEARUSDT", "ALGOUSDT", "GRTUSDT", "EGLDUSDT", "XTZUSDT", "APEUSDT", "FILUSDT", "RUNEUSDT"]

    interval = Client.KLINE_INTERVAL_1DAY #this is a Binance constant (in this case for a 1 day interval)
    #now we iterate over the list of symbols
    for symbol in symbols: 
        fetch_historical_data(symbol, interval)


def categorize_features(file_path):
    """
    Categorize volatility and avg_volume into buckets (High, Medium, Low).
    """
    try:
        data = pd.read_csv(file_path)

        # Categorization of volatility; 
        #OBSERVATION: we asked ChatGPT insights on how to use .qcut
        #to categorize financial data; we then took inspiration from the received insights
        #and came up with the code for our case
        data["volatility_category"] = pd.qcut(data["volatility"],
                                              q=3,
                                              labels=["Low", "Medium", "High"],
                                              duplicates="drop")

        # Now we categorize average volume (by following the same reasoning as the one for volatility)
        data["avg_volume_category"] = pd.qcut(data["avg_volume"],
                                              q=3,
                                              labels=["Low", "Medium", "High"],
                                              duplicates="drop")

        # Finally, we save the updated file
        data.to_csv(file_path, index=False)
        print(f"Updated categories for {file_path}")
    except Exception as e:
        print(f"Failed to process {file_path}: {e}")

#as explained in the docstring, we now apply the categorization implemented by the previous function 
#to all the CSV files in the data directory
def categorize_all_data():
    """
    Apply feature categorization to all CSV files in the data directory.
    """
    for file in os.listdir(DATA_DIR):
        if file.endswith(".csv"):
            categorize_features(os.path.join(DATA_DIR, file))

#we ensure that the code is executed as main program
if __name__ == "__main__":
    fetch_all_data()
    categorize_all_data()
