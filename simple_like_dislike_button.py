import streamlit as st

#also here, problems are related to the fact that some variables result as not-defined since
#I separated this part from the main script; in the main script, it would work

#we initialize session_state for the coin preference
if "coin_preference" not in st.session_state:
    st.session_state["coin preference"] = []

#creation of button to like the tracked coin 
if st.button(f"👍Add {selected_coin} to liked coins", key=f"likes_{selected_coin}"):
    st.session_state["coin_preference"] = {"liked_coin": selected_coin, 
                                           "feedback": "liked"} 
                                           #"feedback":"liked" stores coin preference in session_state
    
#creation of button to dislike the tracked coin
if st.button(f"👎Add {selected_coin} to disliked coins", key=f"dislikes_{selected_coin}"):
    st.session_state["coin_preference"] = {"disliked_coin": selected_coin,
                                           "feedback": "disliked"} 

#adding a brief section to show the user the expressed preference
# FEEDBACK PART of format string DOES NOT WORK
# st.write(f"{selected_coin} is now a coin you {"coin_preference"["feedback"]}")
