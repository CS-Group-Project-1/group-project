import streamlit as st
import pandas as pd
from utils import fetch_historical_data, calculate_percentage_change, plot_candlestick

# Function to handle coin search and analysis
def show_coin_search():
    """
    This function displays the coin search page.
    It allows users to select a cryptocurrency, 
    set analysis parameters, and view the results.
    """
    
    # Title for the search page
    st.title("Coin Search and Analysis")

    # Dropdown to select the cryptocurrency
    st.subheader("Step 1: Select a Coin")
    coin = st.selectbox("Choose a cryptocurrency", ["BTC", "ETH", "SOL", "ADA", "XRP"], index=0)

    # Dropdown to select the time interval for analysis
    st.subheader("Step 2: Select Time Interval")
    interval = st.selectbox("Choose an interval", ["1m", "5m", "1h", "1d", "1w", "1M"], index=3)

    # Input box to set the threshold for percentage change
    st.subheader("Step 3: Set Percentage Threshold")
    threshold = st.number_input("Enter a percentage threshold (%)", min_value=0.0, step=0.1, value=1.0)

    # Button to analyze the selected coin
    if st.button("Analyze"):
        st.write(f"Analyzing {coin} over a {interval} interval with a {threshold}% threshold...")

        # Fetch historical data using a utility function
        historical_data = fetch_historical_data(coin, interval)

        # Check if data was successfully fetched
        if historical_data is not None:
            # Calculate the percentage change
            percentage_change = calculate_percentage_change(historical_data)
            st.write(f"Percentage Change: {percentage_change:.2f}%")

            # Display whether the criteria is met
            if percentage_change >= threshold:
                st.success(f"The percentage change meets or exceeds the threshold of {threshold}%.")
            else:
                st.error(f"The percentage change is below the threshold of {threshold}%.")

            # Plot the candlestick chart for visualization
            st.subheader(f"{coin} Historical Performance")
            plot_candlestick(historical_data, coin, interval)
        else:
            st.error(f"Failed to fetch data for {coin}. Please try again later.")

    # Feedback section
    st.markdown("---")
    st.subheader("What do you think about this coin?")
    col1, col2 = st.columns(2)
    if col1.button("👍 Like"):
        st.session_state["feedback"] = {"coin": coin, "liked": 1}
        st.success("Thank you for your feedback!")
    if col2.button("👎 Dislike"):
        st.session_state["feedback"] = {"coin": coin, "liked": 0}
        st.success("Thank you for your feedback!")
