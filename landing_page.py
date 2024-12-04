import streamlit as st

def show_landing_page():
    """
    This function renders the landing page of the application.
    """
    # Title and Introduction
    st.title("Welcome to Easy2Trade!")
    st.markdown("""
    ## Quick Overview
    Easy2Trade is your go-to tool for analyzing cryptocurrency trends, tracking coins, 
    and receiving personalized recommendations based on your preferences.
    
    ### Key Features:
    - **Search and Analyze Coins**: Evaluate coin performance using candlestick charts and metrics.
    - **Feedback-Based Recommendations**: Like or dislike coins to receive tailored suggestions.
    - **Track Coins**: Manage your custom watchlist and set your own thresholds for alerts.
    """)

    # Candlestick Chart Explanation
    st.markdown("""
    ## Understanding Candlestick Charts
    Candlestick charts represent the price movement of a cryptocurrency over a specific timeframe.
    For instance:
    - **1D (1 Day)**: Each candlestick represents the price data for one day.
    - **1H (1 Hour)**: Each candlestick represents one hour of trading.

    ### How a Candlestick is Formed:
    - **Open Price**: The price at which the asset started trading in the given timeframe.
    - **Close Price**: The price at which the asset finished trading in the given timeframe.
    - **High Price**: The highest price reached in the timeframe.
    - **Low Price**: The lowest price reached in the timeframe.

    Below is a visual explanation of a candlestick structure:
    """)
    st.image("candlestick_example.jpg", caption="Example of a Candlestick Chart (Source: https://learn.bybit.com/candlestick/best-candlestick-patterns/)")

    # Technical Details Section
    st.markdown("""
    ## Technical Details
    Easy2Trade uses a **Machine Learning (ML) Model** to provide personalized recommendations based on user feedback. 
    Here’s how the process works:
    1. **User Feedback**: When you like or dislike a coin, this feedback is recorded and influences future recommendations.
    2. **Attributes Considered**:
       - **Volatility**: Measures price fluctuations.
       - **Average Volume**: Tracks the average amount traded.
       - **Trends**: Classifies patterns like "Upward", "Downward", or "Stable".
    3. **Prediction of Unrated Coins**: The ML model calculates scores for unrated coins and ranks them for suggestions.
    """)

    # Supported Coins for ML Recommendations
    st.markdown("""
    ## Supported Coins for Recommendations
    The following coins are currently supported for the recommendation algorithm:
    - BTCUSDT, ETHUSDT, ADAUSDT, SOLUSDT, XRPUSDT, MATICUSDT, DOGEUSDT, SHIBUSDT, ARBUSDT, OPUSDT,
      AVAXUSDT, ATOMUSDT, DOTUSDT, LINKUSDT, LTCUSDT, BNBUSDT, UNIUSDT, AAVEUSDT, SANDUSDT, 
      MANAUSDT, AXSUSDT, FTMUSDT, NEARUSDT, ALGOUSDT, GRTUSDT, EGLDUSDT, XTZUSDT, APEUSDT, 
      FILUSDT, RUNEUSDT.
      
    ### Expanding the Data
    If you wish to expand the list of supported coins, please contact:
    **robin.grob@student.unisg.ch**
    """)

    # Limitations Section
    st.markdown("""
    ## Limitations
    - **Manually Added Coins**: Coins added manually (not in the initial dataset) are not considered by the recommendation algorithm.
    - **Feedback Constraints**: The model relies on sufficient user feedback to make accurate predictions.
    - **Data Refresh**: Ensure the `processed_data.csv` file is synchronized regularly for the best results.
    """)

    # Footer
    st.markdown("---")
    st.markdown("""
    #### Easy2Trade - Developed as part of a group project. 
    Explore the crypto world with confidence and ease!
    """)
