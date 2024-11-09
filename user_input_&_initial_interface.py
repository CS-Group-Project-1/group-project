#necessary imports
import streamlit as st 
#if / when we decide to use json: import json



#the following code lines serve to set up the interface
st.title("Easy2Trade")
st.header("header saying some things")
st.subheader("subheader saying some other things") #only if we want both a header & a subheader /one of them

st.write("Easy2Trade is a tool that will very much facilitate the search and analysis of different types of coins")
st.write("To get started, please specify your choice for the following criteria.")


#if we need to use st.session, state, 
# before defining the form, we initialize the session state which will allow us to temporary store input variables
if 'user_input' not in st.session_state:
    st.session_state.user_input = {}

#we set up a form for the selection of coin, interval and percentage change threshold 
with st.form("User Input Form"):
    coin_selection = st.selectbox("Select a coin", ["Bitcoin", "Ethereum", "Solana", "XRP", "Cardano"])
    interval_selection = st.selectbox("Select an interval", ["Minutes", "Hours", "Days"])
    percentage_threshold = st.number_input("Insert a percentage")
    st.form_submit_button('Submit choices')
#WE HAVE TO CHECK IF THIS MAKES SENSE AGAIN, I PUT THE NAMES OF THE COINS & INTERVALS AS STRINGS BUT IDK IF IT'S RIGHT




#now we want to store the inputs in a dictionary
if st.form_submit_button('Submit choices'):
    user_input = {'coin':coin_selection, 'interval':interval_selection, 'percentage threshold':percentage_threshold}




#Some things to observe:
#I saw that st.session_state can be useful to temporarily store data (also in case of reruns, ...); 
# however I am not really sure about how it works, so I did not use it for now; we might want to explore it


#The next lines are other options which we could use to write the code

#instaed of writing each sentence with which criteria has been selected, we could create a json dictionary 
#(not sure about how it would look like rxactly though)::
#st.write("You selected the following criteria")
#st.json(user_input)


#this is another way that we could use to create input fields without using streamlit's form module, but it's probably less functional:
#coin_selection = st.selectbox("Select a coin", [Bitcoin, Ethereum, Solana, XRP, Cardano])
#st.write("You selected:", coin_selection)

#interval_selection = st.selectbox("Select an interval", [Minutes, Hours, Days]) #we allow the user to select an interval
#st.write("Your selected time interval is:", interval_selection)

#percentage_threshold = st.number_input("Insert a percentage", min_value = 0.0%) #we allow the user to specify the percentage change threshold
#st.write("The selected percentage threshold is", percentage_threshold)

#initialization of a dictionary to store the user's input
#user_input = {'coin':coin_selection, 'interval':interval_selection, 'percentage threshold':percentage_threshold}
#if we want to convert it in json format: st.json(user_input)


#to finalize the form, we create buttons: option to submit choices or clear everything and restart
#st.button("Confirm choices") 
#st.button("Clear") (we might want to create the option to clear everything)

#if Confirm choices is chosen
#if st.button("Confirm choices"):
    #user_submission = user_input

#if "Clear" is chosen
#if st.button("Clear"):
    #find a way to clear everything