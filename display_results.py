#in this section there are some very preliminary things that we could use 
#to display the results of the analyses; we will have to / could create a table;
#also, we will definitely have to create a graph
#basically here I just wrote some notes in a very draft-like form to start consider 
#how we could develop this



#we create a function to evaluate if the percentage change in the value of the coin 
#surpasses the threshold or not
def check_threshold(initial_value, end_value, percentage_threshold):
    percentage_change = ((end_value - initial_value) / initial value) * 100
    if percentage_change > percentage_threshold:
        print("The percentage change in the value of the coin surpasses the selected threshold")
    elif percentage_change < percentage_threshold:
        print("The percentage change in the value of the coin is smaller than the selected threshold")
    else:
        print("The percentage change in the value of the coin is equal to the threshold")
# I am not sure whether this function is completely correct, I chose initial_value & end_value just to have an idea about how to set up 
#the formula; we would probably have to insert some variable names depending on the rest of the code that handles input from the API etc.



#the following serves to display the results in a functional table format
#st.write("Results for coin:", coin_selection)
#st.table() 
# #FIGURE OUT WHICH PARAMETERS THERE ARE IN THE TABLE --> WHICH DATAFRAME TO USE?); 
# --> ADD COIN SYMBOL, PERCENTAGE CHANGE, THEN THRESHOLD MET OR NOT --> use check_threshold function, 
# ADD COLOR CODING)

#WE ALSO NEED TO CREATE SOME DATA VISUALIZATION, BUT WITH WHAT? 
#use for example st.line_chart() to create graph
