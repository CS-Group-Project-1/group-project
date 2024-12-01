import streamlit as st
import pandas as pd
import os
import requests
from ml_model import MLModel


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


# Initialize and train the ML model
ml_model = MLModel("data/processed_data.csv")  # Pointing to the processed dataset


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

    # Separate liked and disliked coins
    feedback_data = st.session_state["feedback_data"]
    liked_coins = feedback_data[feedback_data["liked"] > 0]
    disliked_coins = feedback_data[feedback_data["liked"] < 0]

    # Display liked coins
    st.subheader("Liked Coins")
    if not liked_coins.empty:
        for _, row in liked_coins.iterrows():
            col1, col2 = st.columns([8, 2])
            col1.write(f"{row['coin']} (Score: {row['liked']})")
            if col2.button("❌ Remove", key=f"remove_liked_{row['coin']}"):
                st.session_state["feedback_data"] = feedback_data[feedback_data["coin"] != row['coin']]
                save_feedback_data()
                st.rerun()
    else:
        st.info("No liked coins yet. Add one below!")

    # Display disliked coins
    st.subheader("Disliked Coins")
    if not disliked_coins.empty:
        for _, row in disliked_coins.iterrows():
            col1, col2 = st.columns([8, 2])
            col1.write(f"{row['coin']} (Score: {row['liked']})")
            if col2.button("❌ Remove", key=f"remove_disliked_{row['coin']}"):
                st.session_state["feedback_data"] = feedback_data[feedback_data["coin"] != row['coin']]
                save_feedback_data()
                st.rerun()
    else:
        st.info("No disliked coins yet. Add one below!")

    # Recommendations based on feedback
    st.subheader("Recommendations")
    if not liked_coins.empty:
        st.write("Based on your liked coins, you might like these:")
        recommendations = ml_model.recommend_coins(user_feedback=liked_coins["coin"].tolist())
        for rec in recommendations:
            st.write(f"- {rec}")
    else:
        st.info("Like some coins to get recommendations!")
