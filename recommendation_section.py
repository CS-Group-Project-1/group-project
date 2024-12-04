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
        processed_data["coin_base"] = processed_data["coin"].str.replace("USDT", "", regex=False).str.strip()
        for _, row in feedback_data.iterrows():
            coin = row["coin"]
            liked = row["liked"]
            if coin in processed_data["coin_base"].values:
                processed_data.loc[processed_data["coin_base"] == coin, "liked"] = liked
        # Drop the temporary 'coin_base' column and save the updated file
        processed_data = processed_data.drop(columns=["coin_base"])
        processed_data.to_csv(processed_file, index=False)
        st.success("Processed data synchronized successfully!")
    else:
        st.error("Processed data file not found. Synchronization failed!")


def add_to_search_list(coin):
    """
    Adds a coin to the Coin Search list dynamically.

    Parameters:
    - coin: The coin symbol to add to the search list.
    """
    if "feedback_data" in st.session_state:
        feedback_data = st.session_state["feedback_data"]
        if coin not in feedback_data["coin"].values:
            new_row = pd.DataFrame({"coin": [coin], "liked": [0]})
            feedback_data = pd.concat([feedback_data, new_row], ignore_index=True)
            st.session_state["feedback_data"] = feedback_data
            feedback_data.to_csv("feedback.csv", index=False)
            st.success(f"{coin} added to the search list!")
        else:
            st.warning(f"{coin} is already in the search list.")
    else:
        st.error("Feedback data is not initialized. Please try again.")


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

    # Synchronize feedback with processed data
    if os.path.exists(feedback_file):
        feedback_data = pd.read_csv(feedback_file).dropna()
        synchronize_with_processed_data(feedback_data, processed_file)
    else:
        feedback_data = pd.DataFrame(columns=["coin", "liked"])
        feedback_data.to_csv(feedback_file, index=False)

    # Retrain the model after synchronization
    st.info("Retraining the model with updated data...")
    ml_model.train_model()
    st.success("Model retrained successfully!")

    # Load feedback data
    liked_coins = feedback_data[feedback_data["liked"] > 0]["coin"].tolist()
    current_coins = feedback_data["coin"].tolist()  # List of all coins in feedback

    # Generate recommendations
    if liked_coins:
        st.write("Based on your preferences, you might like these coins:")

        # Get recommendations from the ML model
        recommendations = ml_model.recommend_coins(user_feedback=liked_coins)

        # Filter recommendations to ensure each coin is unique and not in the feedback list
        filtered_recommendations = [
            rec for rec in recommendations if rec not in current_coins
        ]

        if not filtered_recommendations:
            st.info("No new recommendations available at the moment.")
        else:
            for rec in filtered_recommendations:
                col1, col2 = st.columns([8, 2])
                col1.write(f"- {rec}")
                if col2.button(f"➕ Add {rec} to Feedback and Search", key=f"add_{rec}"):
                    # Add the recommended coin to feedback and search
                    add_to_search_list(rec)
    else:
        st.info("Like some coins to get personalized recommendations!")


# Main script functionality (if needed for standalone testing)
if __name__ == "__main__":
    feedback_data_sample = pd.DataFrame({"coin": ["BTC", "ETH"], "liked": [1, 2]})
    synchronize_with_processed_data(feedback_data_sample, "data/processed_data.csv")
