import streamlit as st

# In this section, we gather all the text elements that the user will see in the landing page.
#Precisely, there are different sections that explain, respectively, the following:
# - the overall goal and functionality of the application;
# - what a candlestick chart is (this is very useful for users who are not very experienced in trading);
# - a section dedicated to briefly explain the machine learning approach used in the app, alongside
#   the supported coins;
# - finally, the limitations of the machine learning model in dealing with manually added coins, 
#   in relation to feedback constraints as well as to the refresh of data (which refers to the need of 
#   synchronizing regularly the 'processed_data.csv` file)

def show_landing_page():
    """
    This function renders the landing page of the application.
    """
    # Title and introduction
    # in the following lines, as well as in other instances of the code where it applies,
    #we use the '##' to make the words right after correspond to a second level header (in case 
    #there were three '###', it would be a third level header).
    # The '**' will make the text appear in bold
    st.title("Easy2Trade")
    st.header("Where Trading Research Speeds Up Faster Than Your Coffee Cools Down")
    st.markdown("""
    ## Quick Overview
    Easy2Trade is your go-to tool for analyzing cryptocurrency trends, tracking coins, 
    and receiving personalized recommendations based on your preferences.
    
    ### The Problem
    Navigating the world of cryptocurrency can be overwhelming, especially for beginners 
    and casual investors. With hundreds of coins, complex charts, and ever-changing trends, 
    it’s hard to know where to start, which coins to track, or how to make informed decisions 
    without extensive research and expertise. 
                
    ### The Solution
    Easy2Trade simplifies cryptocurrency analysis and empowers users to make smarter decisions. 
    By offering an intuitive platform, it allows you to:
    - Analyze coin performance with candlestick charts and clear metrics.
    - Receive personalized recommendations tailored to your preferences through our machine learning model.
    - Stay on top of the market by tracking coins and setting custom alerts. Whether you’re a beginner exploring crypto 
    or an enthusiast looking to refine your strategy, Easy2Trade provides the tools and insights you need to navigate 
    the crypto world with confidence and ease.
    
    ### Key Features:
    - **Search and Analyze Coins**: Evaluate coin performance using candlestick charts and metrics.
    - **Feedback-Based Recommendations**: Like or dislike coins to receive tailored suggestions.
    - **Track Coins**: Manage your custom watchlist and set your own thresholds for alerts.
    """)

    # Candlestick chart explanation: basic notions needed to comprehend what a candlestick chart is
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

    #Explanation of the percentage threshold
    st.markdown("""
    ## Understanding Percentage Thresholds 
    The percentage threshold is a customizable alert setting that notifies you 
    when a cryptocurrency’s price changes by a specific percentage. 
    For example, if you set a 5% threshold, you’ll be alerted when the coin’s price rises or falls 
    by a percentage greater or equal to 5%. 
    This helps you stay informed about significant market movements without constantly monitoring the charts.
    """)

    # Section with technical details about the machine learning part
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

    # Now we list the coins that are supported for the ML Recommendations
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

    # Limitations (of the machine learning part) Section
    st.markdown("""
    ## Limitations
    - **Manually Added Coins**: Coins added manually (not in the initial dataset) are not considered by the recommendation algorithm.
    - **Feedback Constraints**: The model relies on sufficient user feedback to make accurate predictions.
    - **Refresh of Data**: Ensure the `processed_data.csv` file is synchronized regularly for the best results.
    """)

    # Footer of the landing page
    st.markdown("---")
    st.markdown("""
    #### Easy2Trade - Developed as part of a group project. 
    Explore the crypto world with confidence and ease!
    """)
