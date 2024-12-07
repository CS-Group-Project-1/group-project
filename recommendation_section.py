import os
import pandas as pd
import streamlit as st
from ml_model import MLModel

#This file will allow to display the recommendation section. First, we take some necessary steps for data synchronization;
#then we briefly define a function to add coins to the search list.
#After that, we refer to the machine learning (ML) model implemented in the file that has the same name;
#the function that does this will ultimately display the recommendation section, providing coin suggestions
#for the user depending on the given feedback


#as visible in the docstring, the following function is used for synchronizing the feedback data with the processed_data.csv file
def synchronize_with_processed_data(feedback_data, processed_file):
    """
    Synchronizes the feedback data with the processed_data.csv file.

    Parameters:
    - feedback_data: DataFrame containing the feedback data (coin, liked).
    - processed_file: Path to the processed_data.csv file.
    """
    if os.path.exists(processed_file):
        processed_data = pd.read_csv(processed_file) #if the path exists, the file is read into a dataframe
        # Update the "liked" column in processed_data based on feedback
        processed_data["coin_base"] = processed_data["coin"].str.replace("USDT", "", regex=False).str.strip()
        for _, row in feedback_data.iterrows(): #we use '_' as a placeholder when iterating over the rows of the feedback data
            coin = row["coin"]
            liked = row["liked"]
            if coin in processed_data["coin_base"].values:
                processed_data.loc[processed_data["coin_base"] == coin, "liked"] = liked
                #check if the value in the "coin_base"" column and that stored in the coin variable are equal
                #then the value of the 'liked' variable is assigned to the "liked" column in all cases where the 
                #"value in the "coin_base" column and in the coin variable are the same
        # Drop the temporary 'coin_base' column and save the updated file
        processed_data = processed_data.drop(columns=["coin_base"])
        processed_data.to_csv(processed_file, index=False)
        st.success("Processed data synchronized successfully!")
    else:
        st.error("Processed data file not found. Synchronization failed!")

#we define a function to add a coin is dynamically to the coin search list
def add_to_search_list(coin):
    """
    Adds a coin to the Coin Search list dynamically.

    Parameters:
    - coin: The coin symbol to add to the search list.
    """
    if "feedback_data" in st.session_state:
        feedback_data = st.session_state["feedback_data"]
        if coin not in feedback_data["coin"].values:
            new_row = pd.DataFrame({"coin": [coin], "liked": [0]}) #if the coin isn't in the feedback data yet, we create a new row with the coin and the "liked" column defaulting to 0
            feedback_data = pd.concat([feedback_data, new_row], ignore_index=True) #concatenate new row and feedback_data dataframe
            st.session_state["feedback_data"] = feedback_data #update session state
            feedback_data.to_csv("feedback.csv", index=False) #save updated feedback_data in CSV file
            st.success(f"{coin} added to the search list!")
        else:
            st.warning(f"{coin} is already in the search list.")
    else:
        st.error("Feedback data is not initialized. Please try again.")

#the following functions allows to display the recommendation section; here, we use the ML model defined in the dedicated file
def show_recommendations():
    """
    Displays the Recommendations section.
    Provides coin suggestions based on user feedback.
    """
    st.subheader("Recommendations")
    #we define the appropriate files that we will need
    feedback_file = "feedback.csv"
    processed_file = "data/processed_data.csv"

    #Initialize the ML model
    ml_model = MLModel(processed_file)

    #Synchronize feedback with processed data
    if os.path.exists(feedback_file):
        feedback_data = pd.read_csv(feedback_file).dropna()
        synchronize_with_processed_data(feedback_data, processed_file)
    else:
        feedback_data = pd.DataFrame(columns=["coin", "liked"])
        feedback_data.to_csv(feedback_file, index=False)

    #Retrain the model after synchronization
    st.info("Retraining the model with updated data...")
    ml_model.train_model()
    st.success("Model retrained successfully!")

    # Load feedback data
    #in the first of the next two lines, we filter the feedback data so that we only keep the liked coins
    #(which have a value >0 in the "liked" column); then we select the coin column and create a list
    liked_coins = feedback_data[feedback_data["liked"] > 0]["coin"].tolist() 
    current_coins = feedback_data["coin"].tolist()  # List of all coins in feedback

    # Generate recommendations
    if liked_coins:
        st.write("Based on your preferences, you might like these coins:")

        # Get recommendations from the ML model
        recommendations = ml_model.recommend_coins(user_feedback=liked_coins)

        # Filter recommendations to ensure each coin is unique and not in the feedback list
        filtered_recommendations = [
            rec for rec in recommendations if rec not in current_coins
        ]

        if not filtered_recommendations:
            st.info("No new recommendations available at the moment.")
        else:
            for rec in filtered_recommendations:
                col1, col2 = st.columns([8, 2])
                col1.write(f"- {rec}")
                if col2.button(f"➕ Add {rec} to Feedback and Search", key=f"add_{rec}"):
                    # Add the recommended coin to feedback and search
                    add_to_search_list(rec)
    else:
        st.info("Like some coins to get personalized recommendations!")


# Main script functionality; we put it here in case there is a need for it for standalone testing
#(and as in the case of other scripts, with the first line of the next code snippet we ensure that the code below is executed only if the script is run directly/as a main program))
if __name__ == "__main__":
    feedback_data_sample = pd.DataFrame({"coin": ["BTC", "ETH"], "liked": [1, 2]})
    synchronize_with_processed_data(feedback_data_sample, "data/processed_data.csv")
