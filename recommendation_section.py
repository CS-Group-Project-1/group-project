import os
import pandas as pd
import streamlit as st
from ml_model import MLModel


def synchronize_with_processed_data(feedback_data, processed_file):
    """
    Synchronizes the feedback data with the processed_data.csv file.

    Parameters:
    - feedback_data: DataFrame containing the feedback data (coin, liked).
    - processed_file: Path to the processed_data.csv file.
    """
    if os.path.exists(processed_file):
        processed_data = pd.read_csv(processed_file)
        # Update the "liked" column in processed_data based on feedback
        for _, row in feedback_data.iterrows():
            coin = row["coin"]
            liked = row["liked"]
            # Match the coin name in processed_data (remove "USDT" or other suffixes)
            processed_data["coin_base"] = processed_data["coin"].str.replace("USDT", "", regex=False).str.strip()
            if coin in processed_data["coin_base"].values:
                processed_data.loc[processed_data["coin_base"] == coin, "liked"] = liked
        # Drop the temporary 'coin_base' column and save the updated file
        processed_data = processed_data.drop(columns=["coin_base"])
        processed_data.to_csv(processed_file, index=False)
        st.success("Data synchronized successfully!")
    else:
        st.error("Processed data file not found. Synchronization failed!")


def show_recommendations():
    """
    Displays the Recommendations section.
    Provides coin suggestions based on user feedback.
    """
    st.subheader("Recommendations")

    feedback_file = "feedback.csv"
    processed_file = "data/processed_data.csv"

    # Initialize the ML model
    ml_model = MLModel(processed_file)

    # Retrain the model after every update
    if st.button("Retrain Model"):
        ml_model.train_model()
        st.success("Model retrained successfully!") 

    # Load feedback data
    if os.path.exists(feedback_file):
        feedback_data = pd.read_csv(feedback_file).dropna()
        liked_coins = feedback_data[feedback_data["liked"] > 0]["coin"].tolist()
        current_coins = feedback_data["coin"].tolist()  # List of all coins in feedback
    else:
        liked_coins = []
        current_coins = []

    # Generate recommendations
    if liked_coins:
        st.write("Based on your preferences, you might like these coins:")

        # Get recommendations from the ML model
        recommendations = ml_model.recommend_coins(user_feedback=liked_coins)

        # Filter recommendations to ensure each coin is unique and not in the feedback list
        filtered_recommendations = [
            rec for rec in set(recommendations) if rec not in current_coins
        ]

        if not filtered_recommendations:
            st.info("No new recommendations available at the moment.")
        else:
            for rec in filtered_recommendations:
                col1, col2 = st.columns([8, 2])
                col1.write(f"- {rec}")
                if col2.button(f"➕ Add {rec} to Feedback", key=f"add_{rec}"):
                    # Add the recommended coin to feedback
                    new_row = pd.DataFrame({"coin": [rec], "liked": [0]})
                    feedback_data = pd.concat([feedback_data, new_row], ignore_index=True)
                    feedback_data.to_csv(feedback_file, index=False)
                    st.success(f"{rec} added to feedback!")
    else:
        st.info("Like some coins to get personalized recommendations!")
