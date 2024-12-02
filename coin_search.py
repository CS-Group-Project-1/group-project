import streamlit as st
import pandas as pd
import os
from utils import fetch_historical_data, calculate_percentage_change, plot_candlestick

def show_coin_search():
    """
    Displays the Coin Search page for cryptocurrency analysis and feedback.
    """
    st.title("Coin Search and Analysis")

    # Initialize session state variables
    if "binance_symbols" not in st.session_state:
        st.session_state["binance_symbols"] = ["BTC", "ETH", "SOL", "ADA", "XRP"]  # Replace with dynamic fetching logic
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
    if "last_action" not in st.session_state:
        st.session_state["last_action"] = None
    if "feedback_message" not in st.session_state:
        st.session_state["feedback_message"] = None

    feedback_data = st.session_state["feedback_data"]

    # Dropdown to select an existing coin or input a new one
    st.subheader("Step 1: Select or Add a Cryptocurrency")
    existing_coins = feedback_data["coin"].tolist()
    coin = st.selectbox(
        "Previously Liked Cryptocurrency",
        ["Search for a new coin..."] + existing_coins,
        index=0 if st.session_state["current_search_coin"] is None else existing_coins.index(st.session_state["current_search_coin"]) + 1,
    )

    new_coin = st.text_input("Enter Disliked or New Coin Symbol (e.g., BTC, ETH):").strip().upper()

    # Add new coin logic
    if new_coin and new_coin not in st.session_state["binance_symbols"]:
        st.error(f"{new_coin} is not supported by Binance. Please enter a valid coin!")
    elif new_coin and st.button("Add Coin"):
        if new_coin not in existing_coins:
            new_row = pd.DataFrame({"coin": [new_coin], "liked": [0]})
            st.session_state["feedback_data"] = pd.concat([feedback_data, new_row], ignore_index=True)
            st.session_state["feedback_data"].to_csv("feedback.csv", index=False)
            st.session_state["feedback_message"] = ("success", f"{new_coin} has been added successfully!")
            st.session_state["current_search_coin"] = new_coin
            st.rerun()
        else:
            st.warning(f"{new_coin} is already in your list!")

    # Display feedback messages dynamically
    if st.session_state["feedback_message"]:
        message_type, message_text = st.session_state["feedback_message"]
        if message_type == "success":
            st.success(message_text)
        elif message_type == "warning":
            st.warning(message_text)
        elif message_type == "error":
            st.error(message_text)

    # Dropdown to select the time interval for analysis
    st.subheader("Step 2: Select Time Interval")
    interval = st.selectbox("Choose an interval", ["1m", "5m", "1h", "1d", "1w", "1M"], index=3)

    # Input box to set the threshold for percentage change
    st.subheader("Step 3: Set Percentage Threshold")
    threshold = st.number_input("Enter a percentage threshold (%)", min_value=0.0, step=0.1, value=1.0)

    # Analyze button logic
    if st.button("Analyze"):
        if coin == "Search for a new coin...":
            st.error("Please select or input a valid coin!")
            return  # Prevent analysis for invalid selection

        # Initialize start_value with the current liked value of the coin
        if coin in feedback_data["coin"].values:
            st.session_state["start_value"] = feedback_data.loc[feedback_data["coin"] == coin, "liked"].iloc[0]
        else:
            st.session_state["start_value"] = 0  # Default to 0 if the coin is not in the feedback list

        st.session_state["analysis_done"] = True
        st.session_state["current_search_coin"] = coin
        st.session_state["last_analyzed_coin"] = coin  # Update the last analyzed coin
        st.session_state["feedback_message"] = None  # Reset feedback messages
        st.session_state["last_action"] = None  # Reset feedback actions for the new session
        st.write(f"Analyzing {coin} over a {interval} interval with a {threshold}% threshold...")
        historical_data = fetch_historical_data(coin, interval)
        if historical_data is not None:
            st.session_state["historical_data"] = historical_data
            percentage_change = calculate_percentage_change(historical_data)
            st.session_state["percentage_change"] = percentage_change
        else:
            st.error(f"Failed to fetch data for {coin}. Please try again later.")
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
        plot_candlestick(st.session_state["historical_data"], st.session_state["last_analyzed_coin"], interval)

        # Feedback Section
        st.markdown("---")
        st.subheader("What do you think about this coin?")
        col1, col2 = st.columns(2)

        def save_feedback_data():
            st.session_state["feedback_data"].to_csv("feedback.csv", index=False)

                # Ensure start_value is initialized only when the Analyze button is clicked
        if "start_value" not in st.session_state:
            st.session_state["start_value"] = None

        # Like button logic
        if col1.button("👍 Like"):
            if st.session_state["last_action"] == "like":
                st.warning(f"You have already liked {coin} in this search session!")
            else:
                if st.session_state["start_value"] is None:
                    st.error("Analyze the coin first before providing feedback!")
                else:
                    start_value = st.session_state["start_value"]

                    # Compute current_value based on start_value
                    if st.session_state["last_action"] == "dislike":  # Switch from dislike to like
                        current_value = start_value + 1
                    elif start_value + 1 == 0:  # Avoid hitting zero
                        current_value = start_value + 2
                    else:  # Normal like
                        current_value = start_value + 1

                    # Update the feedback data
                    feedback_data.loc[feedback_data["coin"] == coin, "liked"] = current_value
                    save_feedback_data()
                    st.success(f"{coin} liked!")
                    st.session_state["last_action"] = "like"  # Record the action

        # Dislike button logic
        if col2.button("👎 Dislike"):
            if st.session_state["last_action"] == "dislike":
                st.warning(f"You have already disliked {coin} in this search session!")
            else:
                if st.session_state["start_value"] is None:
                    st.error("Analyze the coin first before providing feedback!")
                else:
                    start_value = st.session_state["start_value"]

                    # Compute current_value based on start_value
                    if st.session_state["last_action"] == "like":  # Switch from like to dislike
                        current_value = start_value - 1
                    elif start_value - 1 == 0:  # Avoid hitting zero
                        current_value = start_value - 2
                    else:  # Normal dislike
                        current_value = start_value - 1

                    # Update the feedback data
                    feedback_data.loc[feedback_data["coin"] == coin, "liked"] = current_value
                    save_feedback_data()
                    st.error(f"{coin} disliked!")
                    st.session_state["last_action"] = "dislike"  # Record the action
