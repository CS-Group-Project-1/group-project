import os
import pandas as pd
import numpy as np
from binance.client import Client
from datetime import datetime, timedelta

# Binance API credentials (replace with your own or leave blank if not needed)
API_KEY = ""
API_SECRET = ""

# Initialize Binance Client
client = Client(API_KEY, API_SECRET)

# Directory to save data
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

def fetch_historical_data(symbol, interval, lookback="1 year ago"):
    """
    Fetch historical data from Binance and save it as a CSV file.
    Includes volatility and average volume calculations.
    """
    try:
        # Fetch historical klines
        klines = client.get_historical_klines(symbol, interval, lookback)

        # Convert to DataFrame
        df = pd.DataFrame(klines, columns=[
            "timestamp", "open", "high", "low", "close", "volume", "close_time",
            "quote_asset_volume", "number_of_trades", "taker_buy_base_asset_volume",
            "taker_buy_quote_asset_volume", "ignore"
        ])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df["close"] = df["close"].astype(float)
        df["volume"] = df["volume"].astype(float)

        # Calculate volatility (rolling standard deviation of % changes)
        df["volatility"] = df["close"].pct_change().rolling(window=7).std() * 100

        # Calculate average volume (rolling mean)
        df["avg_volume"] = df["volume"].rolling(window=7).mean()

        # Add trend (Upward, Downward, Stable)
        df["trend"] = np.where(df["close"].diff() > 0, "Upward",
                               np.where(df["close"].diff() < 0, "Downward", "Stable"))

        # Keep relevant columns
        df = df[["timestamp", "close", "volume", "volatility", "avg_volume", "trend"]]

        # Save to CSV
        save_path = f"{DATA_DIR}/{symbol}.csv"
        df.to_csv(save_path, index=False)
        print(f"Data for {symbol} saved to {save_path}")
    except Exception as e:
        print(f"Failed to fetch data for {symbol}: {e}")


def fetch_all_data():
    """
    Fetch historical data for a predefined list of symbols.
    """
    symbols = ["BTCUSDT", "ETHUSDT", "ADAUSDT", "SOLUSDT", "XRPUSDT", "MATICUSDT", "DOGEUSDT", "SHIBUSDT", "ARBUSDT", "OPUSDT", "AVAXUSDT", "ATOMUSDT", "DOTUSDT", "LINKUSDT", "LTCUSDT", "BNBUSDT", "UNIUSDT", "AAVEUSDT", "SANDUSDT", "MANAUSDT", "AXSUSDT", "FTMUSDT", "NEARUSDT", "ALGOUSDT", "GRTUSDT", "EGLDUSDT", "XTZUSDT", "APEUSDT", "FILUSDT", "RUNEUSDT"]

    interval = Client.KLINE_INTERVAL_1DAY

    for symbol in symbols:
        fetch_historical_data(symbol, interval)


def categorize_features(file_path):
    """
    Categorize volatility and avg_volume into buckets (High, Medium, Low).
    """
    try:
        data = pd.read_csv(file_path)

        # Categorize volatility
        data["volatility_category"] = pd.qcut(data["volatility"],
                                              q=3,
                                              labels=["Low", "Medium", "High"],
                                              duplicates="drop")

        # Categorize average volume
        data["avg_volume_category"] = pd.qcut(data["avg_volume"],
                                              q=3,
                                              labels=["Low", "Medium", "High"],
                                              duplicates="drop")

        # Save the updated file
        data.to_csv(file_path, index=False)
        print(f"Updated categories for {file_path}")
    except Exception as e:
        print(f"Failed to process {file_path}: {e}")


def categorize_all_data():
    """
    Apply feature categorization to all CSV files in the data directory.
    """
    for file in os.listdir(DATA_DIR):
        if file.endswith(".csv"):
            categorize_features(os.path.join(DATA_DIR, file))


if __name__ == "__main__":
    fetch_all_data()
    categorize_all_data()
