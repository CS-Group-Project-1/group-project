import streamlit as st
import pandas as pd
import os
import requests
from utils import fetch_historical_data, calculate_percentage_change, plot_candlestick

#This file contains the elements that build the 'COIN SEARCH' page of the application.
#It includes, to illustrate buttons to add or remove the coin, to kickstart the analysis and the buttons to
# like or dislike a coin (relevant also for our machine learnong approach), as well as
#the function that will allow us to display the graph defined in utils.
#A relevant observation is that this file's first function is in great part almost identical to the function 
# #with the same name present in the file 'tracked_coins_page.py' (to precise, we write the definition
# of said function in both scripts for convenience-related reasons; indeed, this way we were able to handle
# the logic of the scripts in an optimal way, furthermore being able to adjust some aspects of the 
# function according to the needs of the specific script if needed; lastly, we observe that we used the same
# names, once again, for clarity and convenience).


#we start by defining a function that will fetch the symbols that are appropriate for the Binance API
def fetch_binance_symbols():
    """
    The function fetches the list of supported symbols from Binance API.
    it returns a list of coins.
    """
    try:
        response = requests.get("https://api.binance.com/api/v3/exchangeInfo")
        response.raise_for_status() #helps to handle HTTP errors
        data = response.json() #formatting with json
        # We filter the API response and keep only symbols ending with 'USDT' in order to fetch coins
        symbols = [symbol["symbol"][:-4] for symbol in data["symbols"] if symbol["symbol"].endswith("USDT")]
        return list(set(symbols))  # We remove duplicates with 'set'
    except Exception as e:
        st.error("Failed to fetch Binance symbols. Please try again later.") #we raise a streamlit error if an exception is encountered
        return ["BTC", "ETH", "SOL", "ADA", "XRP"]  # A list of default fallback coins is returned if 
        #an error is encountered (what is returned differs from the similar function in the 'tracked_coins_page.py'
        # file; in that case, what is returned is an empty list)

#We provide an explanation of the list comprehension used for the definition of the symbols variable;
#this same explanation is also given in the 'coin_serach.py' file
# #when defining the symbols variable, we use '.endswith' because we only want symbols that entail a processed 
# pair in a form analogous to, for example,'BTCUSDT' (we do not want any other ending that differs from 'USDT');
#however, we then do not want USDT to remain visible in the symbol of the coin. This is why we use 
#slicing ('[:-4]') to remove the last 4 characters of all the strings. Coming back to the previous example,
#slicing would let us go from 'BTCUSDT' to 'BTC'


#now we define an extensive function that entails everything we need for the 'COIN SEARCH' page of the app
def show_coin_search():
    """
    Displays the Coin Search page, geared towards cryptocurrency analysis and feedback.
    """
    st.title("Coin Search and Analysis")

    # We initialize the session state keys / variables 
    # OBSERVATION: as in other parts of the code where applicable, we asked ChatGPT a comprehensive 
    #explanation on how to use 'st.session_state' in general terms. We then came up with the appropriate
    #code for our own application
    if "binance_symbols" not in st.session_state:
        st.session_state["binance_symbols"] = fetch_binance_symbols()
        #i.e., if no item corresponding to "binance_symbols" is found in session_state, the function
        #'fetch_binance_symbols' is called in order to initialize the mentioned key

    if "feedback_data" not in st.session_state: #if nothing corresponding to 'feedback_data' is found in session state, we do the following
        feedback_file = "feedback.csv" #we analyze whether this file exists
        if os.path.exists(feedback_file): #we check if the file exists thanks to 'os.path.exists'
            st.session_state["feedback_data"] = pd.read_csv(feedback_file).dropna() #if it exists, we initialize 
            #a dataframe with 'pd.read_csv'; we remove non-existent values with '.dropna()'
        else:
            st.session_state["feedback_data"] = pd.DataFrame(columns=["coin", "liked"])
            #in case the if clause does not apply, a dataframe with columns "coin" and "liked" is initialized

    if "current_search_coin" not in st.session_state: 
        st.session_state["current_search_coin"] = None #we initialize 'current_search_coin' to 'None'

    if "last_analyzed_coin" not in st.session_state: 
        st.session_state["last_analyzed_coin"] = None #we initialize 'last_analyzed_coin' to 'None'

    if "analysis_done" not in st.session_state:
        st.session_state["analysis_done"] = False #we initialize the default value 'False' for 'analysis_done' (key related to the completion of the analysis)

    if "percentage_change" not in st.session_state:
        st.session_state["percentage_change"] = None #we initialize 'percentage_change' to 'None'

    if "last_action" not in st.session_state:
        st.session_state["last_action"] = None #we initialize 'last_action' to 'None' (refers to the last action made by the user)

    if "start_value" not in st.session_state:
        st.session_state["start_value"] = None #we initialize 'start_value' to 'None'

    if "feedback_message" not in st.session_state:
        st.session_state["feedback_message"] = None #we initialize 'feedback_message' to 'None'

    if "selected_interval" not in st.session_state:
        st.session_state["selected_interval"] = "1d" #by default, the interval that the user will select is initialized to '1d'

    if "selected_threshold" not in st.session_state:
        st.session_state["selected_threshold"] = 1.0 #by default, the (percentage) threshold selected by the user 
        #is initialized to 1.0

    #to access the feedback data more easily, we define a local variable that extracts  it (the feedback data) from 'st.session_state'
    feedback_data = st.session_state["feedback_data"] 

    # Dropdown to display the existing list of coins
    st.subheader("Step 1: Manage Your Cryptocurrency List")
    existing_coins = feedback_data["coin"].tolist() #we want to get a list from the dataframe column
    #In the following selectbox, we want to make a small precisation about the options paramter, namely
    #that we concatenated (by using '+') the iterable "search for a new coin" with the dynamic 
    # variable "existing_coins"
    selected_coin = st.selectbox(
        "Previously Added Coins",
        ["Search for a new coin..."] + existing_coins,
        index=0 if st.session_state["current_search_coin"] is None else existing_coins.index(st.session_state["current_search_coin"]) + 1,
    ) #OBSERVATION: we asked ChatGPT to come up with the last line of code (starting from index ...)
    #specifically, we asked it how to dynamically preselect an option in a Streamlit selectbox based 
    #on a value stored in st.session_state
    
    

    # Logic for adding or removing a coin (user can input coin symbols)
    coin_action = st.text_input("Enter Coin Symbol to Add or Remove (e.g., BTC, ETH):").strip().upper()
    #.strip() removes any white spaces at the beginning/end of the string;
    #.upper() gives us the string with all uppercase

    #We now divide the layout in two columns, both with the same width (represented by the relative widths [1,1])
    col1, col2 = st.columns([1, 1])

    # briefly, we define a function to clear the old feedback messages before showing a new one
    def clear_feedback_message():
        st.session_state["feedback_message"] = None

    # Logic of the add button; we create said button in the first column
    if col1.button("Add Coin"):
        clear_feedback_message()
        if not coin_action:
            st.error("Please enter a valid coin symbol!") #signals the user that no coin symbol was entered
        elif coin_action not in st.session_state["binance_symbols"]:
            st.error(f"{coin_action} is not supported by Binance. Please enter a valid coin!") #signals that the entered coin is not valid
        elif coin_action in existing_coins:
            st.warning(f"{coin_action} is already in your list!") #in case the input coin is already part of the existing coins
        else:
            new_row = pd.DataFrame({"coin": [coin_action], "liked": [0]}) #the first row of the liked column is initialized with the value 0
            st.session_state["feedback_data"] = pd.concat([feedback_data, new_row], ignore_index=True) #we concatenate the new row dataframe to feedback_data
            st.session_state["feedback_data"].to_csv("feedback.csv", index=False) #now we add feedback_data to a .csv file
            st.session_state["feedback_message"] = ("success", f"{coin_action} has been added successfully!")
            st.session_state["current_search_coin"] = coin_action #make it so that the coin input by the user is in the "current_search_coin" key of st.session_state
            st.success(f"Coin {coin_action} added to the list!")  # Success message
            st.rerun()

    # Logic of the remove button, which we create in the second column
    if col2.button("Remove Coin"):
        clear_feedback_message()
        if not coin_action:
            st.warning("Please enter a coin symbol to remove!") #in case the user didn't input a coin symbol
        elif coin_action in existing_coins:
            st.session_state["feedback_data"] = feedback_data[feedback_data["coin"] != coin_action] #we remove the row in case the coin is equal to coin_action (input by the user)
            st.session_state["feedback_data"].to_csv("feedback.csv", index=False) #we save the now updated feedback_data into a .csv file
            st.session_state["feedback_message"] = ("success", f"{coin_action} has been removed successfully!")
            if st.session_state["current_search_coin"] == coin_action:
                st.session_state["current_search_coin"] = None #we checked whether the coin that we removed corresponds to "current_search_coin" in the session state; if that's the case we return 'None'
            st.success(f"Coin {coin_action} removed from the list!")  # Success message
            st.rerun()
        else:
            st.error(f"{coin_action} is not in your list and cannot be removed!")

    # Display feedback messages dynamically
    if st.session_state["feedback_message"]:
        message_type, message_text = st.session_state["feedback_message"] #we expect to have a tuple in this instance of session state;
        #the message type we expect is generally "success", "warning", or "error
        if message_type == "success":
            st.success(message_text)
        elif message_type == "warning":
            st.warning(message_text)
        elif message_type == "error":
            st.error(message_text)

    # Dropdown to select the time interval for analysis
    st.subheader("Step 2: Select Time Interval")
    interval = st.selectbox(
        "Choose an interval",
        ["1m", "5m", "1h", "1d", "1w", "1M"],
        index=["1m", "5m", "1h", "1d", "1w", "1M"].index(st.session_state["selected_interval"]), 
        key="interval_dropdown",
    )
    #in the line of code with index = (...), we want to obtain the position (indeed, the index) of a value 
    #in the list of intervals, which we expect to find in st.session_state


    # Creation of input box to set the threshold for percentage change
    st.subheader("Step 3: Set Percentage Threshold")
    threshold = st.number_input(
        "Enter a percentage threshold (%)",
        min_value=0.0,
        step=0.1,
        value=st.session_state["selected_threshold"],
    )

    # Logic of analyze button, this button starts the analysis of the coin data considering the relevant criteria and inputs
    if st.button("Analyze"):
        if selected_coin == "Search for a new coin...":
            st.error("Please select or input a valid coin!")
            return

        #we do the necessary adjustments to session_state
        st.session_state["analysis_done"] = True
        st.session_state["current_search_coin"] = selected_coin
        st.session_state["last_analyzed_coin"] = selected_coin
        st.session_state["feedback_message"] = None
        st.session_state["last_action"] = None
        st.session_state["start_value"] = (
            feedback_data.loc[feedback_data["coin"] == selected_coin, "liked"].iloc[0]
            if selected_coin in feedback_data["coin"].values
            else 0
        ) # In the session state, we set the initial "liked" value for the selected coin
         # If the selected coin exists in the "coin" column of the feedback_data DataFrame, we want to 
         # retrieve the first "liked" value by using .iloc[0].In case the selected coin was not found, 
         # the "liked" value would default to 0
        st.session_state["selected_interval"] = interval
        st.session_state["selected_threshold"] = threshold

        st.write(f"Analyzing {selected_coin} over a {interval} interval with a {threshold}% threshold...")
        historical_data = fetch_historical_data(selected_coin, interval) #we call the function that we defined in utils file
        if historical_data is not None:
            st.session_state["historical_data"] = historical_data #initialize the historical data in session state
            percentage_change = calculate_percentage_change(historical_data) #we call the function defined in the utils file
            st.session_state["percentage_change"] = percentage_change #intialize percentage change in session state
            if abs(percentage_change) >= threshold:
                st.success(f"Threshold met! Percentage change: {percentage_change:.2f}%") #we are checking whether the threshold has been met
            else:
                st.info(f"Threshold not met. Percentage change: {percentage_change:.2f}%")
        else:
            st.error(f"Failed to fetch data for {selected_coin}. Please try again later.") #raises error if it was not possible to get the historical data
            st.session_state["historical_data"] = None
            st.session_state["percentage_change"] = None



    # Display chart and feedback options if analysis is done
    if st.session_state.get("analysis_done") and st.session_state.get("historical_data") is not None:
        percentage_change_display = (
            f"Percentage Change: {st.session_state['percentage_change']:.2f}%"
            if st.session_state["percentage_change"] is not None
            else "Percentage Change: N/A"
        )
        st.subheader(f"{st.session_state['last_analyzed_coin']} Historical Performance")
        st.caption(percentage_change_display)
        plot_candlestick(st.session_state["historical_data"], st.session_state["last_analyzed_coin"], st.session_state["selected_interval"])
        #the plot_candlestick function comes from the utils.py file


        # Feedback Section
        st.markdown("---")
        st.subheader("What do you think about this coin?")
        col1, col2 = st.columns(2) #again, we want to column with equal width, this time we use a shorter way

        #we save the feedback data in the appropriate.csv file
        def save_feedback_data():
            st.session_state["feedback_data"].to_csv("feedback.csv", index=False)
                    
        # Logic of the like button 
        if col1.button("👍 Like"):
            if st.session_state["last_action"] == "like":
                st.warning(f"You have already liked {selected_coin} in this search session!") #check whether the user already liked the coin
            else:
                # Ensure that start_value is preserved and valid, which applies if the analysis  of the coin was already made
                if st.session_state["start_value"] is None:
                    st.error("Analyze the coin first before providing feedback!")
                else:
                    start_value = st.session_state["start_value"]  # Fixed starting value by setting it to the intial "liked" value for the coin initialized in session state

                    # Compute current_value based on start_value
                    if st.session_state["last_action"] == "dislike":  # Switch from dislike to like in case the user previously disliked the coin in question
                        current_value = start_value + 1 
                    elif start_value + 1 == 0:  # Avoid hitting zero (relevant for preventing mistakes)
                        current_value = start_value + 2
                    else:  # Normal like
                        current_value = start_value + 1 #we indicate a new like by adding 1 to the starting value

                    # Safeguard: prevent zero recalculation errors; we add this additonal safeguard since it is very important that 0 is never hit
                    if current_value == 0:
                        current_value = start_value + 2

                    # Update the feedback data
                    feedback_data.loc[feedback_data["coin"] == selected_coin, "liked"] = current_value #we filter the dataframe to find the rows where the coin column corresponds 
                    save_feedback_data()                                                               #to the selected coin; we then assign the 'current_value' to the "liked" column
                    st.success(f"{selected_coin} liked!")
                    st.session_state["last_action"] = "like"  # Record the action

        # Logic of the dislike button (there are various analogies with the logic of the like button)
        if col2.button("👎 Dislike"):
            if st.session_state["last_action"] == "dislike":
                st.warning(f"You have already disliked {selected_coin} in this search session!")
            else:
                # Ensure start_value is preserved and valid (as explained before, for this to apply the analysis needs to have been done)
                if st.session_state["start_value"] is None:
                    st.error("Analyze the coin first before providing feedback!")
                else:
                    start_value = st.session_state["start_value"]  # Again, we set a fixed starting value

                    # Compute current_value based on start_value
                    if st.session_state["last_action"] == "like":  # Switch from like to dislike in case the coin was previously liked by the user
                        current_value = start_value - 1
                    elif start_value - 1 == 0:  # Avoid hitting zero (relevant for preventing mistakes)
                        current_value = start_value - 2
                    else:  # Normal dislike
                        current_value = start_value - 1 #dislikes are represented by a -1

                    # Safeguard: prevent zero recalculation errors; we add this condition because it's very important not to hit 0
                    if current_value == 0:
                        current_value = start_value - 2 #now we have -2 because for the dislikes we want to have negative values

                    # Update the feedback data
                    feedback_data.loc[feedback_data["coin"] == selected_coin, "liked"] = current_value #again, we filter the dataframe
                    save_feedback_data()
                    st.error(f"{selected_coin} disliked!")
                    st.session_state["last_action"] = "dislike"  # Record the action
