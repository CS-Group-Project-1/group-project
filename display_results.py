



#necessary imports (we might have to eliminate this when we unify all code)
import streamlit as st
import pandas as pd



#we simulate an example data frame 
coin_results = {
    'coins':coins,
    'initial_value':[30000, 3000, 2000, 4000,  4500],
    'end_value':[31000, 3500, 2900, 4000, 4300]
}

df = pd.DataFrame(coin_results)

#now we calculate the percentage change in the value of the coin and add it as a column to the dataframe

df['percentage_change'] = ((df['end_value']-df['initial_value']) / df['initial_value'])*100

#add another column that says whether percentage threshold has been surpassed
#met means that the percentage change has NOT surpassed the threshold; 
#not met means that the percentage change has been surpassed

def check_threshold():
    if df['percentage_change'] <= threshold:
        print("Met")
    elif df['percentage_change'] > threshold:
        print("Not met")
   

df['percentage_threshold_criteria'] = check_threshold()



#we define the function that will allow to color code column that evaluates whether threshold has 
#been met or not

def background_color(r):
    color = 'background-color: green' if r else 'red'
    return f'background-color:{color}'

#now format the dataframe
df_colors = df.style.map(background_color, subset=['percentage_threshold_criteria'])


#allowing streamlit to display the result
st.write("Results of the analysis for your selected coin(s)")
st.dataframe(df)

#later, we will also have to create a graph --> we could use st.line_chart
