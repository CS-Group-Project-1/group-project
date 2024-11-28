import streamlit as st
import pandas as pd
import requests 
from datetime import datetime
import plotly.graph_objects as go


#selected coin refers to the coin selected in the user input, here it gives a mistake because 
#obviously the rest of the script is separated from this draft
def create_graph_data():
    symbol = f"{selected_coin}USDT" 
    url = f'https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}'
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

graph_data = create_graph_data()


#to create the graph, we first need to convert our API response (previously converted in JSON)
#in a pandas dataframe
cd = pd.DataFrame(graph_data) #created provisionary dataframe with necessary columns from API
#now we create the dataframe that we actually use for the candlestick graph, i.e.
#that only keeps useful columns
df = cd[["timestamp", "open", "high", "low", "close"]]
#cd['Date'] = pd.to_datetime(cd['Date']) #checking if the date is in the correct datetime format

#title for the graph
st.title("Candlestick graph")
st.write("This graph shows you the candlesticks for your selected coin")

#before creating the graph, we make sure that data is in the correct format 
#by using pandas .astype() function
df["timestamp"] = pd.to_datetime(df["timestamp"], unit = "ms")
df["open"] = df["open"].astype(float)
df["high"] = df["high"].astype(float)
df["low"] = df["low"].astype(float)
df["close"] = df["close"].astype(float)


figure_candlesticks = go.Figure(data=[go.Candlestick(x=df["timestamp"],
                                      open = df["open"],
                                      high = df["high"],
                                      low = df["low"],
                                      close = df["close"])])

#this code allows us to display the different candlesticks in a graph
#open, high, low and close all refer to the price of the coin (i.e., price of the coin at opening,
#highest and lowest price reached by the coin, and finally closing price)
#the code for the candlestick graph was made following the instructions 
#from the plotly library (https://plotly.com/python/candlestick-charts/)

#we display the chart in streamlit
st.plotly_chart(figure_candlesticks)