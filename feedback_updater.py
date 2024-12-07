import pandas as pd

#This file is solely dedicated to the definition of a function that allows to
#update the feedback column that was added to the dataframes (depending on the Likes and Dislikes that are part of the feedback) 


def update_feedback(coin, feedback):
    """
    Updates the 'liked' column for a specific coin in the dataset.
    :param coin: The coin symbol (e.g., "BTCUSDT").
    :param feedback: +1 for like, -1 for dislike.
    """
    data_path = "data/processed_data.csv" #we identify where the (CSV) data is located

    try:
        # We load the CSV files (datasets) into a pandas dataframe
        data = pd.read_csv(data_path)

        # Check if the coin exists (specifically, we look into the "coin" column of the dataframe)
        if coin not in data["coin"].values:
            print(f"Coin {coin} not found in the dataset.") #we print an error message if the coin doesn't exist
            return

        # Update the 'liked' column
        current_liked_value = data.loc[data["coin"] == coin, "liked"].values[0]
        if feedback == 1:  # Like 
            data.loc[data["coin"] == coin, "liked"] = current_liked_value + 1
        elif feedback == -1:  # Dislike
            data.loc[data["coin"] == coin, "liked"] = max(current_liked_value - 1, -1)  # Prevent going below -1 by using the max function
        #The first line of this code block filters the dataframe for the row where the "coin" matches the input
        #thanks to .values[0], the value of the "liked" column for the coin in question is extracted
        

        # Save the updated dataset
        data.to_csv(data_path, index=False) #save data to CSV file
        print(f"Feedback for {coin} updated. Current liked value: {data.loc[data['coin'] == coin, 'liked'].values[0]}")

    except FileNotFoundError:
        print(f"Dataset not found at {data_path}. Please ensure the file exists.") #raise error in case the database does not exist
    except Exception as e:
        print(f"An error occurred: {e}") #for errors in general

# Example usage (and we further ensure that the code below is executed only if the script is run directly/as a main program)
if __name__ == "__main__":
    coin_to_update = input("Enter the coin symbol to update (e.g., BTCUSDT): ").strip().upper()
    feedback_value = int(input("Enter feedback (+1 for like, -1 for dislike): "))
    update_feedback(coin_to_update, feedback_value)
