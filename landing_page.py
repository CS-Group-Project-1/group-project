import streamlit as st

def show_landing_page():
    """
    This function renders the landing page of the application.
    """
    # Display the title and description
    st.title("Welcome to Easy2Trade!")
    st.markdown("""
    ## What is Easy2Trade?
    Easy2Trade is a tool designed to help you analyze cryptocurrency trends, 
    track coins based on your custom criteria, and receive recommendations 
    tailored to your preferences.

    ### Features:
    - **Search and Analyze Coins**: Select a coin, analyze its trends, and see how it performs over time.
    - **Feedback-Based Recommendations**: Like or dislike analyzed coins, and the bot will recommend coins you might prefer.
    - **Track Coins**: Add coins to your tracked list and get notifications when your criteria are met.
    """)

    # Footer
    st.markdown("---")
    st.caption("Developed as part of a group project. Enjoy exploring the crypto world with Easy2Trade!")
