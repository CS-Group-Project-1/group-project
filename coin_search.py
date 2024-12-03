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
    if "start_value" not in st.session_state:
        st.session_state["start_value"] = None
    if "feedback_message" not in st.session_state:
        st.session_state["feedback_message"] = None

    feedback_data = st.session_state["feedback_data"]

    # Dropdown to display the existing list of coins
    st.subheader("Step 1: Manage Your Cryptocurrency List")
    existing_coins = feedback_data["coin"].tolist()
    selected_coin = st.selectbox(
        "Previously Added Coins",
        ["Search for a new coin..."] + existing_coins,
        index=0 if st.session_state["current_search_coin"] is None else existing_coins.index(st.session_state["current_search_coin"]) + 1,
    )

    # Logic for adding or removing a coin
    coin_action = st.text_input("Enter Coin Symbol to Add or Remove (e.g., BTC, ETH):").strip().upper()

    col1, col2 = st.columns([1, 1])

    # Clear old feedback messages before showing a new one
    def clear_feedback_message():
        st.session_state["feedback_message"] = None

    # Add button logic
    if col1.button("Add Coin"):
        clear_feedback_message()  # Clear old messages
        if not coin_action:
            st.error("Please enter a valid coin symbol!")
        elif coin_action not in st.session_state["binance_symbols"]:
            st.error(f"{coin_action} is not supported by Binance. Please enter a valid coin!")
        elif coin_action in existing_coins:
            st.warning(f"{coin_action} is already in your list!")
        else:
            new_row = pd.DataFrame({"coin": [coin_action], "liked": [0]})
            st.session_state["feedback_data"] = pd.concat([feedback_data, new_row], ignore_index=True)
            st.session_state["feedback_data"].to_csv("feedback.csv", index=False)
            st.session_state["feedback_message"] = ("success", f"{coin_action} has been added successfully!")
            st.session_state["current_search_coin"] = coin_action
            st.rerun()

    # Remove button logic
    if col2.button("Remove Coin"):
        clear_feedback_message()  # Clear old messages
        if not coin_action:
            st.warning("Please enter a coin symbol to remove!")
        elif coin_action in existing_coins:
            st.session_state["feedback_data"] = feedback_data[feedback_data["coin"] != coin_action]
            st.session_state["feedback_data"].to_csv("feedback.csv", index=False)
            st.session_state["feedback_message"] = ("success", f"{coin_action} has been removed successfully!")
            if st.session_state["current_search_coin"] == coin_action:
                st.session_state["current_search_coin"] = None  # Reset current search coin if it matches
            st.rerun()
        else:
            st.error(f"{coin_action} is not in your list and cannot be removed!")

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
        if selected_coin == "Search for a new coin...":
            st.error("Please select or input a valid coin!")
            return  # Prevent analysis for invalid selection

        st.session_state["analysis_done"] = True
        st.session_state["current_search_coin"] = selected_coin
        st.session_state["last_analyzed_coin"] = selected_coin  # Update the last analyzed coin
        st.session_state["feedback_message"] = None  # Reset feedback messages
        st.session_state["last_action"] = None  # Reset feedback actions for the new session
        st.session_state["start_value"] = feedback_data.loc[feedback_data["coin"] == selected_coin, "liked"].iloc[0] if selected_coin in feedback_data["coin"].values else 0  # Initialize start value
        st.write(f"Analyzing {selected_coin} over a {interval} interval with a {threshold}% threshold...")
        historical_data = fetch_historical_data(selected_coin, interval)
        if historical_data is not None:
            st.session_state["historical_data"] = historical_data
            percentage_change = calculate_percentage_change(historical_data)
            st.session_state["percentage_change"] = percentage_change
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
        plot_candlestick(st.session_state["historical_data"], st.session_state["last_analyzed_coin"], interval)

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
