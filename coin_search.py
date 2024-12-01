import streamlit as st
import pandas as pd
import os
from utils import fetch_historical_data, calculate_percentage_change, plot_candlestick

def show_coin_search():
    """
    Displays the Coin Search page for cryptocurrency analysis and feedback.
    """
    st.title("Coin Search and Analysis")

    # Fetch Binance-supported symbols
    if "binance_symbols" not in st.session_state:
        st.session_state["binance_symbols"] = ["BTC", "ETH", "SOL", "ADA", "XRP"]  # Replace with dynamic fetching logic

    # Load feedback data
    feedback_file = "feedback.csv"
    if "feedback_data" not in st.session_state:
        if os.path.exists(feedback_file):
            st.session_state["feedback_data"] = pd.read_csv(feedback_file).dropna()
        else:
            st.session_state["feedback_data"] = pd.DataFrame(columns=["coin", "liked"])

    feedback_data = st.session_state["feedback_data"]

    # Dropdown to select an existing coin or input a new one
    st.subheader("Step 1: Select or Add a Cryptocurrency")
    existing_coins = feedback_data["coin"].tolist()
    coin = st.selectbox("Previously Liked Cryptocurrency", ["Search for a new coin..."] + existing_coins)

    new_coin = st.text_input("Enter Disliked or New Coin Symbol (e.g., BTC, ETH):").strip().upper()

    # Add new coin logic
    if new_coin and new_coin not in st.session_state["binance_symbols"]:
        st.error(f"{new_coin} is not supported by Binance. Please enter a valid coin!")
    elif new_coin and st.button("Add Coin"):
        if new_coin not in existing_coins:
            new_row = pd.DataFrame({"coin": [new_coin], "liked": [0]})
            st.session_state["feedback_data"] = pd.concat([feedback_data, new_row], ignore_index=True)
            st.session_state["feedback_data"].to_csv(feedback_file, index=False)
            st.success(f"{new_coin} added to your list!")
            st.experimental_rerun()
        else:
            st.warning(f"{new_coin} is already in your list!")

    # Dropdown to select the time interval for analysis
    st.subheader("Step 2: Select Time Interval")
    interval = st.selectbox("Choose an interval", ["1m", "5m", "1h", "1d", "1w", "1M"], index=3)

    # Input box to set the threshold for percentage change
    st.subheader("Step 3: Set Percentage Threshold")
    threshold = st.number_input("Enter a percentage threshold (%)", min_value=0.0, step=0.1, value=1.0)

    # Analyze button logic
    if st.button("Analyze"):
        st.session_state["analysis_done"] = True
        st.session_state["selected_coin"] = coin
        st.write(f"Analyzing {coin} over a {interval} interval with a {threshold}% threshold...")
        historical_data = fetch_historical_data(coin, interval)
        if historical_data is not None:
            st.session_state["historical_data"] = historical_data
            percentage_change = calculate_percentage_change(historical_data)
            st.session_state["percentage_change"] = percentage_change

            st.write(f"Percentage Change: {percentage_change:.2f}%")
            plot_candlestick(historical_data, coin, interval)

            st.session_state["feedback_message"] = None  # Reset feedback messages
        else:
            st.error(f"Failed to fetch data for {coin}. Please try again later.")
            st.session_state["historical_data"] = None
            st.session_state["percentage_change"] = None

    # Display chart and feedback options if analysis is done
    if st.session_state.get("analysis_done") and st.session_state.get("historical_data") is not None:
        st.subheader(f"{coin} Historical Performance")
        plot_candlestick(st.session_state["historical_data"], coin, interval)

        # Feedback Section
        st.markdown("---")
        st.subheader("What do you think about this coin?")
        col1, col2 = st.columns(2)

        def save_feedback_data():
            st.session_state["feedback_data"].to_csv(feedback_file, index=False)

        # Like button logic
        if col1.button("👍 Like"):
            if coin in feedback_data["coin"].values:
                feedback_data.loc[feedback_data["coin"] == coin, "liked"] += 1
                st.success(f"{coin} liked! Its score has been updated.")
            else:
                new_row = pd.DataFrame({"coin": [coin], "liked": [1]})
                st.session_state["feedback_data"] = pd.concat([feedback_data, new_row], ignore_index=True)
                st.success(f"{coin} added to Liked Coins!")
            save_feedback_data()

        # Dislike button logic
        if col2.button("👎 Dislike"):
            if coin in feedback_data["coin"].values:
                feedback_data.loc[feedback_data["coin"] == coin, "liked"] -= 1
                st.error(f"{coin} disliked! Its score has been updated.")
            else:
                new_row = pd.DataFrame({"coin": [coin], "liked": [-1]})
                st.session_state["feedback_data"] = pd.concat([feedback_data, new_row], ignore_index=True)
                st.error(f"{coin} added to Disliked Coins!")
            save_feedback_data()

    # Display feedback messages dynamically
    if "feedback_message" in st.session_state and st.session_state["feedback_message"]:
        message_type, message_text = st.session_state["feedback_message"]
        if message_type == "success":
            st.success(message_text)
        elif message_type == "error":
            st.error(message_text)
