import requests
import streamlit as st

# Function to fetch historical price data and calculate percentage change
def fetch_and_analyze_data(coin, interval, limit, threshold):
    symbol = f"{coin}USDT"
    url = f'https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}'
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # Get the opening price of the first candlestick and the closing price of the last candlestick
        open_price = float(data[0][1])  # Open price of the first entry
        close_price = float(data[-1][4])  # Close price of the last entry
        
        # Calculate percentage change
        percentage_change = ((close_price - open_price) / open_price) * 100
        
        # Check if percentage change meets the threshold
        meets_criteria = percentage_change >= threshold
        return percentage_change, meets_criteria
    
    except requests.exceptions.RequestException as e:
        st.warning(f"Error fetching data for {coin}: {e}")
        return None, None

# Streamlit interface
st.title("Crypto Coin Price Analysis")

# User input for coin, interval, limit, and threshold
selected_coin = st.selectbox("Select Coin", options=["BTC", "ETH", "SOL", "XRP", "ADA"], index=0)
interval = st.selectbox("Select Interval", options=["1m", "5m", "1h", "1d"], index=2)
limit = st.number_input("Number of Candlesticks", min_value=1, max_value=10, value=1)
threshold = st.number_input("Percentage Change Threshold", min_value=0.0, value=1.0, step=0.1)

# Fetch data and display results
if st.button("Analyze"):
    percentage_change, meets_criteria = fetch_and_analyze_data(selected_coin, interval, limit, threshold)
    
    if percentage_change is not None:
        st.write(f"Percentage Change over {limit} {interval} interval(s): {percentage_change:.2f}%")
        if meets_criteria:
            st.success(f"The percentage change meets or exceeds the threshold of {threshold}%.")
        else:
            st.error(f"The percentage change is below the threshold of {threshold}%.")