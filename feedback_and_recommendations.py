import streamlit as st
import pandas as pd
import os
from recommendation_section import show_recommendations, synchronize_with_processed_data


def show_feedback_page():
    """
    Displays the Feedback and Synchronization page.
    Allows users to view, manage feedback, and synchronize data.
    """
    st.title("Feedback & Recommendations")

    feedback_file = "feedback.csv"
    processed_file = "data/processed_data.csv"

    # Initialize feedback data
    if "feedback_data" not in st.session_state:
        if os.path.exists(feedback_file):
            feedback_data = pd.read_csv(feedback_file).dropna()
        else:
            feedback_data = pd.DataFrame(columns=["coin", "liked"])
        st.session_state["feedback_data"] = feedback_data

    feedback_data = st.session_state["feedback_data"]

    # Function to save feedback data to the CSV file
    def save_feedback_data():
        st.session_state["feedback_data"].to_csv(feedback_file, index=False)

    # Separate liked and disliked coins
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
                st.success(f"Removed {row['coin']} from liked coins.")
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
                st.success(f"Removed {row['coin']} from disliked coins.")
                st.rerun()
    else:
        st.info("No disliked coins yet. Add one below!")

    # Synchronize with processed_data.csv
    st.subheader("Synchronize Data")
    if st.button("Synchronize with Processed Data"):
        try:
            synchronize_with_processed_data(st.session_state["feedback_data"], processed_file)
            st.success("Data synchronized successfully!")
        except Exception as e:
            st.error(f"Synchronization failed: {str(e)}")

    # Show recommendations at the bottom
    st.markdown("---")
    show_recommendations()


# Main script functionality for standalone testing
if __name__ == "__main__":
    show_feedback_page()
