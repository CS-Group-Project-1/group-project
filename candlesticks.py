#we do the necessary imports

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime 

#definition of which data will be used for the graph; cd stands for candlesticks data

#here an example dataframe will be used to test if it works; then we'll need to be able to link this to the data from the API
#for the specific chosen coin
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


st.plotly_chart(figure_candlesticks)





