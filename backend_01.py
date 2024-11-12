import streamlit as st
import requests

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

# Initialize session state for tracked coins if not already set
if "tracked_coins" not in st.session_state:
    st.session_state["tracked_coins"] = []

# Streamlit interface for user input
st.title("🚀 Easy2Trade: Crypto Coin Price Tracker")

# User input for coin selection and tracking criteria
available_coins = ["BTC", "ETH", "SOL", "XRP", "ADA"]
selected_coin = st.selectbox("Select Coin to Track", available_coins)
interval = st.selectbox("Select Interval", options=["1m", "5m", "1h", "1d"], index=2)
limit = st.number_input("Number of Candlesticks", min_value=1, max_value=10, value=1)
threshold = st.number_input("Percentage Change Threshold (%)", min_value=0.0, value=1.0, step=0.1)

# Button to add coin and criteria to the tracked list
if st.button("Add to Tracked List"):
    st.session_state["tracked_coins"].append({
        "coin": selected_coin,
        "interval": interval,
        "limit": limit,
        "threshold": threshold
    })
    st.success("Tracking criteria added successfully!")

# Displaying the list of tracked coins and analysis results
st.header("📈 Analysis Results")
for idx, criteria in enumerate(st.session_state["tracked_coins"]):
    st.subheader(f"{idx + 1}. {criteria['coin']} - {criteria['interval']} interval")
    st.write(f"Threshold: {criteria['threshold']}% over {criteria['limit']} candlestick(s)")

    # Fetch and analyze data for each tracked coin
    percentage_change, meets_criteria = fetch_and_analyze_data(
        criteria["coin"], criteria["interval"], criteria["limit"], criteria["threshold"]
    )

    # Display the analysis results
    if percentage_change is not None:
        st.write(f"Percentage Change: {percentage_change:.2f}%")
        if meets_criteria:
            st.success("✅ Criteria Met")
        else:
            st.error("❌ Criteria Not Met")
    
    # Options to remove the coin from tracking
    if st.button(f"Remove {criteria['coin']} from tracking", key=f"remove_{idx}"):
        st.session_state["tracked_coins"].pop(idx)
        st.experimental_rerun()  # Refresh the page to update the list

st.write("——" * 10)

