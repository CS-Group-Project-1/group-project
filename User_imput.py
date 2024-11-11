import streamlit as st

# Title and description for the app
st.title("Easy2Trade: Coin Tracking Interface")
st.write("Input your preferred coins, criteria, and tracking settings below.")

# Input fields for user data
# Define the list of available coins
available_coins = ["Bitcoin", "Ethereum", "Solana", "XRP", "Cardano"]

# Multi-select input for coins
coins = st.multiselect("Select coin(s) to track:", available_coins)
threshold = st.number_input("Enter percentage change threshold:", min_value=0.0, step=0.1)
interval = st.selectbox("Select the interval:", ["Minutes", "Hours", "Days"])
candlesticks = st.number_input("Enter number of candlesticks to look back:", min_value=1, step=1)

# Button to submit tracking criteria
if st.button("Add Tracking Criteria"):
    st.write("### Tracking Criteria Summary")
    st.write(f"Coins: {coins}")
    st.write(f"Percentage Change Threshold: {threshold}%")
    st.write(f"Interval: {interval}")
    st.write(f"Candlesticks to look back: {candlesticks}")

# Example of displaying tracked coins (temporary storage for demo)
if "tracked_coins" not in st.session_state:
    st.session_state["tracked_coins"] = []

# Add tracking info to session state
if st.button("Add to Tracked List"):
    st.session_state["tracked_coins"].append({
        "coins": coins,
        "threshold": threshold,
        "interval": interval,
        "candlesticks": candlesticks
    })

# Display currently tracked coins
st.write("### Currently Tracked Coins")
for idx, criteria in enumerate(st.session_state["tracked_coins"]):
    st.write(f"{idx + 1}. Coins: {criteria['coins']}, Threshold: {criteria['threshold']}%, Interval: {criteria['interval']}, Candlesticks: {criteria['candlesticks']}")
