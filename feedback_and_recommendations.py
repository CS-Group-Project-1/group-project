import streamlit as st
import pandas as pd
import os
from recommendation_section import show_recommendations, synchronize_with_processed_data

#With this file, we want to show the app's FEEDBACK AND RECOMMENDATIONS page.
#Crucial elements for the management of the feedback are implemented, such as buttons that
#allow the user to remove the coin from the liked / disliked coins. Crucially,
#the user can also see the feedback given to the coins, i.e. the liked and disliked coins are displayed.
#Crucially, this page also shows the coins that the user might like based on their expressed preference,
#i.e. it shows the recommendations for coins based on the feedback given by the user.
#Further elements handled in this script relate principally to data synchronization.

#we define the function that will concretely display the page in question
def show_feedback_page():
    """
    Displays the Feedback and Synchronization page.
    Allows users to view, manage feedback, and synchronize data.
    """
    st.title("Feedback & Recommendations")
    
    feedback_file = "feedback.csv"
    processed_file = "data/processed_data.csv"

    #Initialize the feedback data
    if "feedback_data" not in st.session_state:
        if os.path.exists(feedback_file):
            feedback_data = pd.read_csv(feedback_file).dropna() #if 'feedback_file' exists, we read it into a dataframe and drop empty columns
        else:
            feedback_data = pd.DataFrame(columns=["coin", "liked"]) #if the file does not exist, we initialize an empty dataframe with the specified columns
        st.session_state["feedback_data"] = feedback_data
    #we ensure to retrieve the 'feedback_data' from session state
    feedback_data = st.session_state["feedback_data"]

    # Function to save feedback data to the CSV file
    def save_feedback_data():
        st.session_state["feedback_data"].to_csv(feedback_file, index=False)

    # Separate liked and disliked coins
    liked_coins = feedback_data[feedback_data["liked"] > 0] #since, as a reminder, "like" corresponds to +1
    disliked_coins = feedback_data[feedback_data["liked"] < 0] #again as a reminder, "dislike" corresponds to -1

    # Display liked coins
    st.subheader("Liked Coins")
    if not liked_coins.empty:
        for _, row in liked_coins.iterrows(): #we use '_' as a placeholder when iterating over the rows of the feedback data
            col1, col2 = st.columns([8, 2]) #we create 2 columns and set the width ratio to 8:2
            col1.write(f"{row['coin']} (Score: {row['liked']})") #we write the name of the coin and its score (-->liked value)
            if col2.button("❌ Remove", key=f"remove_liked_{row['coin']}"): #button that allows to remove the coin from the tracked list
                st.session_state["feedback_data"] = feedback_data[feedback_data["coin"] != row['coin']]
                save_feedback_data() #in the line above, we took out the removed coin from the session state for 'feedback_data', which we then save
                st.success(f"Removed {row['coin']} from liked coins.")
                st.rerun()
    else:
        st.info("No liked coins yet. Add one below!")

    # Display disliked coins; the logic followed is the same as for the display of the liked coins right above
    st.subheader("Disliked Coins")
    if not disliked_coins.empty:
        for _, row in disliked_coins.iterrows(): #we use '_' as a placeholder when iterating over the rows of the feedback data
            col1, col2 = st.columns([8, 2]) #we create 2 columns and set the width ratio to 8:2
            col1.write(f"{row['coin']} (Score: {row['liked']})") #name of the coin and score
            if col2.button("❌ Remove", key=f"remove_disliked_{row['coin']}"): #button to remove the coin from the disliked coins
                st.session_state["feedback_data"] = feedback_data[feedback_data["coin"] != row['coin']]
                save_feedback_data() #removal of coin from session state
                st.success(f"Removed {row['coin']} from disliked coins.")
                st.rerun()
    else:
        st.info("No disliked coins yet. Add one below!")

    # Synchronize with the processed_data.csv file
    st.subheader("Synchronize Data")
    if st.button("Synchronize with Processed Data"):
        try:
            synchronize_with_processed_data(st.session_state["feedback_data"], processed_file)
            st.success("Data synchronized successfully!")
        except Exception as e:
            st.error(f"Synchronization failed: {str(e)}")

    # Show recommendations at the bottom
    st.markdown("---")
    show_recommendations()


# Main script functionality for standalone testing (as in other cases, through the first line we ensure that 
# the code below is executed only if the script is run directly/as a main program)
if __name__ == "__main__":
    show_feedback_page()
