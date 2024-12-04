import streamlit as st
import pandas as pd
import os
import requests
from utils import fetch_historical_data, calculate_percentage_change, plot_candlestick


TRACKED_COINS_FILE = "tracked_coins.csv"


def fetch_binance_symbols():
    """
    Fetches the list of supported symbols from Binance API.
    Returns a list of coins (excluding pairs).
    """
    try:
        response = requests.get("https://api.binance.com/api/v3/exchangeInfo")
        response.raise_for_status()
        data = response.json()
        # Filter and keep only symbols ending with 'USDT' to fetch coins
        symbols = [symbol["symbol"][:-4] for symbol in data["symbols"] if symbol["symbol"].endswith("USDT")]
        return list(set(symbols))  # Remove duplicates
    except Exception as e:
        st.error("Failed to fetch Binance symbols. Please try again later.")
        return ["BTC", "ETH", "SOL", "ADA", "XRP"]  # Default fallback coins


def load_tracked_coins():
    """Load tracked coins from the file."""
    if os.path.exists(TRACKED_COINS_FILE):
        return pd.read_csv(TRACKED_COINS_FILE)
    else:
        return pd.DataFrame(columns=["coin", "threshold"])


def save_tracked_coins(data):
    """Save tracked coins to the file."""
    data.to_csv(TRACKED_COINS_FILE, index=False)


def show_coin_search():
    """
    Displays the Coin Search page for cryptocurrency analysis and feedback.
    """
    st.title("Coin Search and Analysis")

    # Initialize session state variables
    if "binance_symbols" not in st.session_state:
        st.session_state["binance_symbols"] = fetch_binance_symbols()

    if "feedback_data" not in st.session_state:
        feedback_file = "feedback.csv"
        if os.path.exists(feedback_file):
            st.session_state["feedback_data"] = pd.read_csv(feedback_file).dropna()
        else:
            st.session_state["feedback_data"] = pd.DataFrame(columns=["coin", "liked"])

    if "current_search_coin" not in st.session_state:
        st.session_state["current_search_coin"] = None

    if "last_analyzed_coin" not in st.session_state:
        st.session_state["last_analyzed_coin"] = None

    if "analysis_done" not in st.session_state:
        st.session_state["analysis_done"] = False

    if "percentage_change" not in st.session_state:
        st.session_state["percentage_change"] = None

    if "selected_interval" not in st.session_state:
        st.session_state["selected_interval"] = "1d"

    if "selected_threshold" not in st.session_state:
        st.session_state["selected_threshold"] = 1.0

    feedback_data = st.session_state["feedback_data"]

    # Dropdown to display the existing list of coins
    st.subheader("Step 1: Manage Your Cryptocurrency List")
    existing_coins = feedback_data["coin"].tolist()
    selected_coin = st.selectbox(
        "Previously Added Coins",
        ["Search for a new coin..."] + existing_coins,
        index=0 if st.session_state["current_search_coin"] is None else existing_coins.index(st.session_state["current_search_coin"]) + 1,
    )

    # Dropdown to select the time interval for analysis
    st.subheader("Step 2: Select Time Interval")
    interval = st.selectbox(
        "Choose an interval",
        ["1m", "5m", "1h", "1d", "1w", "1M"],
        index=["1m", "5m", "1h", "1d", "1w", "1M"].index(st.session_state["selected_interval"]),
        key="interval_dropdown",
    )

    # Input box to set the threshold for percentage change
    st.subheader("Step 3: Set Percentage Threshold")
    threshold = st.number_input(
        "Enter a percentage threshold (%)",
        min_value=0.0,
        step=0.1,
        value=st.session_state["selected_threshold"],
    )

    # Analyze button logic
    if st.button("Analyze"):
        if selected_coin == "Search for a new coin...":
            st.error("Please select or input a valid coin!")
            return

        st.session_state["analysis_done"] = True
        st.session_state["current_search_coin"] = selected_coin
        st.session_state["last_analyzed_coin"] = selected_coin
        st.session_state["selected_interval"] = interval
        st.session_state["selected_threshold"] = threshold

        st.write(f"Analyzing {selected_coin} over a {interval} interval with a {threshold}% threshold...")
        historical_data = fetch_historical_data(selected_coin, interval)
        if historical_data is not None:
            st.session_state["historical_data"] = historical_data
            percentage_change = calculate_percentage_change(historical_data)
            st.session_state["percentage_change"] = percentage_change
            if abs(percentage_change) >= threshold:
                st.success(f"Threshold met! Percentage change: {percentage_change:.2f}%")
            else:
                st.info(f"Threshold not met. Percentage change: {percentage_change:.2f}%")
                if st.button(f"Track {selected_coin}"):
                    # Add coin to tracked list
                    tracked_coins = load_tracked_coins()
                    if selected_coin not in tracked_coins["coin"].values:
                        new_row = pd.DataFrame({"coin": [selected_coin], "threshold": [threshold]})
                        tracked_coins = pd.concat([tracked_coins, new_row], ignore_index=True)
                        save_tracked_coins(tracked_coins)
                        st.success(f"{selected_coin} added to your tracked coins list!")
                    else:
                        st.warning(f"{selected_coin} is already in your tracked coins list.")
        else:
            st.error(f"Failed to fetch data for {selected_coin}. Please try again later.")
            st.session_state["historical_data"] = None
            st.session_state["percentage_change"] = None




    # Display chart and feedback options if analysis is done
    if st.session_state.get("analysis_done") and st.session_state.get("historical_data") is not None:
        percentage_change_display = (
            f"Percentage Change: {st.session_state['percentage_change']:.2f}%"
            if st.session_state["percentage_change"] is not None
            else "Percentage Change: N/A"
        )
        st.subheader(f"{st.session_state['last_analyzed_coin']} Historical Performance")
        st.caption(percentage_change_display)
        plot_candlestick(st.session_state["historical_data"], st.session_state["last_analyzed_coin"], st.session_state["selected_interval"])


        # Feedback Section
        st.markdown("---")
        st.subheader("What do you think about this coin?")
        col1, col2 = st.columns(2)

        def save_feedback_data():
            st.session_state["feedback_data"].to_csv("feedback.csv", index=False)
                    
        # Like button logic
        if col1.button("👍 Like"):
            if st.session_state["last_action"] == "like":
                st.warning(f"You have already liked {selected_coin} in this search session!")
            else:
                # Ensure start_value is preserved and valid
                if st.session_state["start_value"] is None:
                    st.error("Analyze the coin first before providing feedback!")
                else:
                    start_value = st.session_state["start_value"]  # Fixed starting value

                    # Compute current_value based on start_value
                    if st.session_state["last_action"] == "dislike":  # Switch from dislike to like
                        current_value = start_value + 1
                    elif start_value + 1 == 0:  # Avoid hitting zero
                        current_value = start_value + 2
                    else:  # Normal like
                        current_value = start_value + 1

                    # Safeguard: prevent zero recalculation errors
                    if current_value == 0:
                        current_value = start_value + 2

                    # Update the feedback data
                    feedback_data.loc[feedback_data["coin"] == selected_coin, "liked"] = current_value
                    save_feedback_data()
                    st.success(f"{selected_coin} liked!")
                    st.session_state["last_action"] = "like"  # Record the action

        # Dislike button logic
        if col2.button("👎 Dislike"):
            if st.session_state["last_action"] == "dislike":
                st.warning(f"You have already disliked {selected_coin} in this search session!")
            else:
                # Ensure start_value is preserved and valid
                if st.session_state["start_value"] is None:
                    st.error("Analyze the coin first before providing feedback!")
                else:
                    start_value = st.session_state["start_value"]  # Fixed starting value

                    # Compute current_value based on start_value
                    if st.session_state["last_action"] == "like":  # Switch from like to dislike
                        current_value = start_value - 1
                    elif start_value - 1 == 0:  # Avoid hitting zero
                        current_value = start_value - 2
                    else:  # Normal dislike
                        current_value = start_value - 1

                    # Safeguard: prevent zero recalculation errors
                    if current_value == 0:
                        current_value = start_value - 2

                    # Update the feedback data
                    feedback_data.loc[feedback_data["coin"] == selected_coin, "liked"] = current_value
                    save_feedback_data()
                    st.error(f"{selected_coin} disliked!")
                    st.session_state["last_action"] = "dislike"  # Record the action
