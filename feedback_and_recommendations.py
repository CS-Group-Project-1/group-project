import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier

# Function to display the feedback and recommendation page
def show_feedback_page():
    """
    This function handles user feedback collection and provides coin recommendations
    based on the user's preferences using a Machine Learning model.
    """

    st.title("Feedback and Recommendations")
    
    # Step 1: Collect user feedback
    st.header("Provide Feedback")
    st.markdown("""
        After analyzing coins, let us know what you think about them. 
        Your feedback will help us improve recommendations tailored to your preferences.
    """)

    # Simulate a feedback scenario (you can replace this with actual coin data)
    coin = st.selectbox("Select a coin to provide feedback", ["BTC", "ETH", "SOL", "ADA", "XRP"])
    
    # Like or Dislike buttons
    feedback_col1, feedback_col2 = st.columns(2)
    if feedback_col1.button("👍 Like"):
        save_feedback(coin, liked=1)
        st.success(f"Thanks for liking {coin}!")
    if feedback_col2.button("👎 Dislike"):
        save_feedback(coin, liked=0)
        st.success(f"Thanks for your feedback on {coin}!")

    st.markdown("---")

    # Step 2: Train and Display Recommendations
    st.header("Recommended Coins")
    recommendations = get_recommendations()
    if recommendations is not None:
        st.write("Based on your feedback, you might like these coins:")
        for idx, rec in enumerate(recommendations):
            st.write(f"{idx + 1}. {rec}")
    else:
        st.info("Not enough feedback data yet to generate recommendations. Start by liking or disliking coins!")
        

# Function to save user feedback into a CSV file
def save_feedback(coin, liked):
    """
    Saves user feedback to a CSV file.

    Parameters:
        coin (str): The coin for which feedback is provided (e.g., 'BTC').
        liked (int): Feedback value (1 for Like, 0 for Dislike).
    """
    feedback_file = "feedback.csv"
    new_feedback = {"coin": coin, "liked": liked}

    # Check if the file already exists
    try:
        if feedback_file in st.session_state:
            feedback_data = st.session_state[feedback_file]
        else:
            feedback_data = pd.read_csv(feedback_file)
    except FileNotFoundError:
        # If no file exists yet, create a new DataFrame
        feedback_data = pd.DataFrame(columns=["coin", "liked"])

    # Append the new feedback
    feedback_data = feedback_data.append(new_feedback, ignore_index=True)
    feedback_data.to_csv(feedback_file, index=False)

    # Save the feedback in session state for real-time updates
    st.session_state[feedback_file] = feedback_data


# Function to get recommendations based on user feedback
def get_recommendations():
    """
    Trains a simple ML model using user feedback and provides recommendations.

    Returns:
        list: A list of recommended coins (or None if insufficient data).
    """
    feedback_file = "feedback.csv"
    try:
        # Load feedback data
        feedback_data = pd.read_csv(feedback_file)
        if feedback_data.shape[0] < 5:  # Ensure enough data points to train a model
            return None

        # Feature engineering: Create dummy variables for coins
        feature_data = pd.get_dummies(feedback_data["coin"])
        X = feature_data  # Features are the dummy variables for coins
        y = feedback_data["liked"]  # Target is the feedback (1 = Like, 0 = Dislike)

        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train a simple Logistic Regression model
        model = LogisticRegression()
        model.fit(X_train, y_train)

        # Predict recommendations
        coin_probabilities = model.predict_proba(X_test)[:, 1]  # Get probabilities of "like"
        recommended_coins = X_test.columns[coin_probabilities.argsort()[-3:][::-1]]  # Top 3 coins

        return recommended_coins.tolist()

    except Exception as e:
        print(f"Error in generating recommendations: {e}")
        return None
