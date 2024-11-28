import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
from datetime import datetime 

# Function to fetch historical price data and calculate percentage change
def fetch_and_analyze_data(coin, interval, limit, threshold):
    symbol = f"{coin}USDT"
    url = f'https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}'
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # Get the opening price of the first candlestick and the closing price of the last candlestick
        open_price = float(data[0][1])  # Open price of the first entry
        close_price = float(data[-1][4])  # Close price of the last entry
        
        # Calculate percentage change
        percentage_change = ((close_price - open_price) / open_price) * 100
        
        # Check if percentage change meets the threshold
        meets_criteria = percentage_change >= threshold
        return percentage_change, meets_criteria
    
    except requests.exceptions.RequestException as e:
        st.warning(f"Error fetching data for {coin}: {e}")
        return None, None

# Initialize session state for tracked coins if not already set
if "tracked_coins" not in st.session_state:
    st.session_state["tracked_coins"] = []

# Streamlit interface for user input
st.title("🚀 Easy2Trade: Crypto Coin Price Tracker")

# User input for coin selection and tracking criteria
available_coins = ["BTC", "ETH", "SOL", "XRP", "ADA"]
selected_coin = st.selectbox("Select Coin to Track", available_coins)
interval = st.selectbox("Select Interval", options=["1m", "5m", "1h", "1d"], index=2)
limit = st.number_input("Number of Candlesticks", min_value=1, max_value=10, value=1)
threshold = st.number_input("Percentage Change Threshold (%)", min_value=0.0, value=1.0, step=0.1)

# Button to add coin and criteria to the tracked list
if st.button("Add to Tracked List"):
    st.session_state["tracked_coins"].append({
        "coin": selected_coin,
        "interval": interval,
        "limit": limit,
        "threshold": threshold
    })
    st.success("Tracking criteria added successfully!")

# Displaying the list of tracked coins and analysis results
st.header("📈 Analysis Results")
for idx, criteria in enumerate(st.session_state["tracked_coins"]):
    st.subheader(f"{idx + 1}. {criteria['coin']} - {criteria['interval']} interval")
    st.write(f"Threshold: {criteria['threshold']}% over {criteria['limit']} candlestick(s)")

    # Fetch and analyze data for each tracked coin
    percentage_change, meets_criteria = fetch_and_analyze_data(
        criteria["coin"], criteria["interval"], criteria["limit"], criteria["threshold"]
    )

    # Display the analysis results
    if percentage_change is not None:
        st.write(f"Percentage Change: {percentage_change:.2f}%")
        if meets_criteria:
            st.success("✅ Criteria Met")
        else:
            st.error("❌ Criteria Not Met")
    
    # Options to remove the coin from tracking
    if st.button(f"Remove {criteria['coin']} from tracking", key=f"remove_{idx}"):
        st.session_state["tracked_coins"].pop(idx)
        st.rerun()  # Refresh the page to update the list

st.write("——" * 10)



#data visualization: implementation of candlesticks graph
#we do the necessary imports: (keeping this note here so that we know what was used for the graph)
#import streamlit as st
#import pandas as pd
#import plotly.graph_objects as go
#from datetime import datetime 

#definition of which data will be used for the graph; cd stands for candlesticks data

#here an example dataframe will be used to test if it works; 
#then we'll need to be able to link this to the data from the API for the specific chosen coin


example_data = {
    "Date": ['2024-11-18','2024-11-19','2024-11-20', '2024-11-21', '2024-11-22'],
    "BTC.Open": [34000, 36500, 33000, 38000, 37500],
    "BTC.High": [35000, 37000, 34000, 38500, 39000],
    "BTC.Low": [33000, 36000, 32500, 37000, 36500],
    "BTC.Close": [34300, 36800, 33900, 38100, 37700]
}

cd = pd.DataFrame(example_data) #created dataframe from example data for testing of the graph
cd['Date'] = pd.to_datetime(cd['Date']) #checking if the date is in the correct datetime format

#title for the graph
st.title("Candlestick graph")
st.write("This graph shows you the candlesticks for your selected coin")

figure_candlesticks = go.Figure(data=[go.Candlestick(x=cd['Date'],
                                      open = cd['BTC.Open'],
                                      high = cd['BTC.High'],
                                      low = cd['BTC.Low'],
                                      close = cd['BTC.Close'])])
#this code allows us to display the different candlesticks in a graph
#open, high, low and close all refer to the price of the coin (i.e., price of the coin at opening,
#highest and lowest price reached by the coin, and finally closing price)
#the code for the candlestick graph was made following the instructions 
#from the plotly library (https://plotly.com/python/candlestick-charts/)

#we display the created candlestick chart in streamlit
st.plotly_chart(figure_candlesticks)




#we initialize the session state for the coin preference; 
#this section will allow the user to add the coin to liked coins or to disliked coins

if "coin_preference" not in st.session_state:
    st.session_state["coin_preference"] = []

#creation of button to like the tracked coin and the selected parameters
if st.button(f"👍Add {selected_coin} to liked coins", key=f"likes_{selected_coin}_{interval}_{limit}_{threshold}"):
    st.session_state["coin_preference"] = {"liked_coin": selected_coin,
                                           "liked_interval": interval,
                                           "liked_limit": limit,
                                           "liked_threshold": threshold, 
                                           "feedback": "liked"}
    
#creation of button to dislike the tracked coin
if st.button(f"👎Add {selected_coin} to disliked coins", key=f"dislikes_{selected_coin}"):
    st.session_state["coin_preference"] = {"disliked_coin": selected_coin,
                                           "disliked_interval": interval,
                                           "disliked_limit": limit,
                                           "disliked_threshold": threshold,
                                           "feedback": "disliked"}
    
#adding a brief section to show the user the expressed preference
#feedback part of format string DOES NOT WORK:
# st.write(f"{selected_coin} is now a coin you {"coin_preference"["feedback"]}")
# this basically works but I do not think that it is dependent on which button you choose:
# st.write(f"{interval}, {limit}, {threshold} are your preferred criteria.")



