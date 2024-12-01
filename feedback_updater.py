import pandas as pd

def update_feedback(coin, feedback):
    """
    Updates the 'liked' column for a specific coin in the dataset.
    :param coin: The coin symbol (e.g., "BTCUSDT").
    :param feedback: +1 for like, -1 for dislike.
    """
    data_path = "data/processed_data.csv"

    try:
        # Load the dataset
        data = pd.read_csv(data_path)

        # Check if the coin exists
        if coin not in data["coin"].values:
            print(f"Coin {coin} not found in the dataset.")
            return

        # Update the 'liked' column
        current_liked_value = data.loc[data["coin"] == coin, "liked"].values[0]
        if feedback == 1:  # Like
            data.loc[data["coin"] == coin, "liked"] = current_liked_value + 1
        elif feedback == -1:  # Dislike
            data.loc[data["coin"] == coin, "liked"] = max(current_liked_value - 1, -1)  # Prevent going below -1

        # Save the updated dataset
        data.to_csv(data_path, index=False)
        print(f"Feedback for {coin} updated. Current liked value: {data.loc[data['coin'] == coin, 'liked'].values[0]}")

    except FileNotFoundError:
        print(f"Dataset not found at {data_path}. Please ensure the file exists.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    coin_to_update = input("Enter the coin symbol to update (e.g., BTCUSDT): ").strip().upper()
    feedback_value = int(input("Enter feedback (+1 for like, -1 for dislike): "))
    update_feedback(coin_to_update, feedback_value)
