import streamlit as st
import pandas as pd
import os
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

    # Initialize session state to track selected coin, analysis status, and historical data
    if "selected_coin" not in st.session_state:
        st.session_state["selected_coin"] = None
    if "analysis_done" not in st.session_state:
        st.session_state["analysis_done"] = False
    if "historical_data" not in st.session_state:
        st.session_state["historical_data"] = None
    if "percentage_change" not in st.session_state:
        st.session_state["percentage_change"] = None

    # Dropdown to select the cryptocurrency
    st.subheader("Step 1: Select a Coin")
    coin = st.selectbox("Choose a cryptocurrency", ["BTC", "ETH", "SOL", "ADA", "XRP"], index=0)

    # Reset session state if the selected coin changes
    if coin != st.session_state["selected_coin"]:
        st.session_state["selected_coin"] = coin
        st.session_state["analysis_done"] = False  # Reset analysis status
        st.session_state["historical_data"] = None
        st.session_state["percentage_change"] = None

    # Dropdown to select the time interval for analysis
    st.subheader("Step 2: Select Time Interval")
    interval = st.selectbox("Choose an interval", ["1m", "5m", "1h", "1d", "1w", "1M"], index=3)

    # Input box to set the threshold for percentage change
    st.subheader("Step 3: Set Percentage Threshold")
    threshold = st.number_input("Enter a percentage threshold (%)", min_value=0.0, step=0.1, value=1.0)

    # Button to analyze the selected coin
    if st.button("Analyze"):
        st.session_state["analysis_done"] = True
        st.write(f"Analyzing {coin} over a {interval} interval with a {threshold}% threshold...")

        # Fetch historical data using a utility function
        historical_data = fetch_historical_data(coin, interval)

        # Check if data was successfully fetched
        if historical_data is not None:
            # Save data and percentage change to session state
            st.session_state["historical_data"] = historical_data
            st.session_state["percentage_change"] = calculate_percentage_change(historical_data)

            # Display the percentage change
            percentage_change = st.session_state["percentage_change"]
            st.write(f"Percentage Change: {percentage_change:.2f}%")

            # Display whether the criteria is met
            if percentage_change >= threshold:
                st.success(f"The percentage change meets or exceeds the threshold of {threshold}%.")
            else:
                st.error(f"The percentage change is below the threshold of {threshold}%.")

        else:
            st.error(f"Failed to fetch data for {coin}. Please try again later.")

    # Display the chart and analysis if analysis is done
    if st.session_state["analysis_done"] and st.session_state["historical_data"] is not None:
        st.subheader(f"{coin} Historical Performance")
        plot_candlestick(st.session_state["historical_data"], coin, interval)

        # Feedback section
        st.markdown("---")
        st.subheader("What do you think about this coin?")
        col1, col2 = st.columns(2)

        # Initialize feedback CSV and session state
        feedback_file = "feedback.csv"
        if "feedback_data" not in st.session_state:
            if os.path.exists(feedback_file):
                feedback_data = pd.read_csv(feedback_file).dropna()
            else:
                feedback_data = pd.DataFrame(columns=["coin", "liked"])
            st.session_state["feedback_data"] = feedback_data

        # Function to save feedback data to the CSV file
        def save_feedback_data():
            st.session_state["feedback_data"].to_csv(feedback_file, index=False)

        # Handle the Like button
        if col1.button("👍 Like"):
            feedback_data = st.session_state["feedback_data"]
            if coin in feedback_data["coin"].values:
                st.warning(f"{coin} is already in your feedback list!")
            else:
                # Add the coin to the liked list
                new_row = pd.DataFrame({"coin": [coin], "liked": [1]})
                st.session_state["feedback_data"] = pd.concat([feedback_data, new_row], ignore_index=True)
                save_feedback_data()
                st.success(f"{coin} added to Liked Coins!")

        # Handle the Dislike button
        if col2.button("👎 Dislike"):
            feedback_data = st.session_state["feedback_data"]
            if coin in feedback_data["coin"].values:
                st.warning(f"{coin} is already in your feedback list!")
            else:
                # Add the coin to the disliked list
                new_row = pd.DataFrame({"coin": [coin], "liked": [0]})
                st.session_state["feedback_data"] = pd.concat([feedback_data, new_row], ignore_index=True)
                save_feedback_data()
                st.success(f"{coin} added to Disliked Coins!")
