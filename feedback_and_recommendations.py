import streamlit as st
import pandas as pd
import os
import requests


def get_binance_symbols():
    """
    Fetches the list of supported symbols from Binance API.
    """
    try:
        response = requests.get("https://api.binance.com/api/v3/exchangeInfo")
        response.raise_for_status()
        data = response.json()
        return [symbol["symbol"][:-4] for symbol in data["symbols"] if symbol["symbol"].endswith("USDT")]
    except Exception as e:
        st.error("Failed to fetch Binance symbols. Please try again later.")
        return []


def show_feedback_page():
    """
    Displays the Feedback and Recommendations page.
    Users can view and manage liked/disliked coins and get recommendations.
    """
    st.title("Feedback & Recommendations")

    # Fetch Binance-supported symbols
    if "binance_symbols" not in st.session_state:
        st.session_state["binance_symbols"] = get_binance_symbols()

    # Initialize session state for feedback data
    if "feedback_data" not in st.session_state:
        feedback_file = "feedback.csv"
        if os.path.exists(feedback_file):
            feedback_data = pd.read_csv(feedback_file).dropna()
        else:
            feedback_data = pd.DataFrame(columns=["coin", "liked"])
        st.session_state["feedback_data"] = feedback_data

    # Function to save feedback data to the CSV file
    def save_feedback_data():
        feedback_file = "feedback.csv"
        st.session_state["feedback_data"].to_csv(feedback_file, index=False)

    # Separate liked and disliked coins
    feedback_data = st.session_state["feedback_data"]
    liked_coins = feedback_data[feedback_data["liked"] == 1]["coin"].tolist()
    disliked_coins = feedback_data[feedback_data["liked"] == 0]["coin"].tolist()

    # Display liked coins
    st.subheader("Liked Coins")
    if liked_coins:
        for coin in liked_coins:
            col1, col2 = st.columns([8, 2])
            col1.write(coin)
            if col2.button("❌ Remove", key=f"remove_liked_{coin}"):
                # Remove the coin from the feedback data
                st.session_state["feedback_data"] = feedback_data[feedback_data["coin"] != coin]
                save_feedback_data()
                st.session_state["feedback_message"] = ""
                st.rerun()  # Refresh the page
    else:
        st.info("No liked coins yet. Add one below!")

    # Display disliked coins
    st.subheader("Disliked Coins")
    if disliked_coins:
        for coin in disliked_coins:
            col1, col2 = st.columns([8, 2])
            col1.write(coin)
            if col2.button("❌ Remove", key=f"remove_disliked_{coin}"):
                # Remove the coin from the feedback data
                st.session_state["feedback_data"] = feedback_data[feedback_data["coin"] != coin]
                save_feedback_data()
                st.session_state["feedback_message"] = ""
                st.rerun()  # Refresh the page
    else:
        st.info("No disliked coins yet. Add one below!")

    # Add new coins
    st.subheader("Add Coins to Liked or Disliked List")
    new_coin = st.text_input("Enter the coin symbol (e.g., BTC, ETH):").strip().upper()

    # Buttons for liking or disliking coins
    col1, col2 = st.columns(2)

    def add_coin_to_feedback(new_coin, liked):
        """
        Function to handle adding a coin to liked or disliked list.
        Handles error messages for duplicate entries, unsupported coins, and empty inputs.
        """
        if not new_coin:  # Check if the input is empty
            st.session_state["feedback_message"] = ("error", "Input cannot be empty. Please enter a valid coin symbol!")
        elif liked and new_coin in liked_coins:
            st.session_state["feedback_message"] = ("warning", f"{new_coin} is already in the Liked Coins list!")
        elif not liked and new_coin in disliked_coins:
            st.session_state["feedback_message"] = ("warning", f"{new_coin} is already in the Disliked Coins list!")
        elif liked and new_coin in disliked_coins:
            st.session_state["feedback_message"] = ("error", f"{new_coin} is already in the Disliked Coins list! Remove it before adding to Liked Coins.")
        elif not liked and new_coin in liked_coins:
            st.session_state["feedback_message"] = ("error", f"{new_coin} is already in the Liked Coins list! Remove it before adding to Disliked Coins.")
        elif new_coin not in st.session_state["binance_symbols"]:
            st.session_state["feedback_message"] = ("error", f"{new_coin} is not supported by Binance. Please enter a valid coin!")
        else:
            # Add to the appropriate list
            new_row = pd.DataFrame({"coin": [new_coin], "liked": [1 if liked else 0]})
            st.session_state["feedback_data"] = pd.concat([feedback_data, new_row], ignore_index=True)
            save_feedback_data()
            st.session_state["feedback_message"] = ("success", f"{new_coin} added to {'Liked' if liked else 'Disliked'} Coins!")
            st.rerun()  # Refresh the page

    # Buttons for adding coins
    if col1.button("👍 Add to Liked Coins"):
        add_coin_to_feedback(new_coin, liked=True)

    if col2.button("👎 Add to Disliked Coins"):
        add_coin_to_feedback(new_coin, liked=False)


    # Display feedback message below the buttons with appropriate styling
    if "feedback_message" in st.session_state and st.session_state["feedback_message"]:
        message_type, message_text = st.session_state["feedback_message"]
        if message_type == "success":
            st.success(message_text)
        elif message_type == "warning":
            st.warning(message_text)
        elif message_type == "error":
            st.error(message_text)

    # Recommendations based on liked coins
    st.subheader("Recommendations")
    if liked_coins:
        st.write("Based on your liked coins, you might like these:")
        recommendations = generate_recommendations(liked_coins)
        for rec in recommendations:
            st.write(f"- {rec}")
    else:
        st.info("Like some coins to get recommendations!")


def generate_recommendations(liked_coins):
    """
    Generates recommendations based on the liked coins.
    This is a placeholder function that suggests other coins.
    """
    all_coins = ["BTC", "ETH", "SOL", "ADA", "XRP", "DOT", "DOGE", "LTC"]
    recommendations = [coin for coin in all_coins if coin not in liked_coins][:3]
    return recommendations
