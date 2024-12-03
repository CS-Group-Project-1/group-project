import os
import pandas as pd

def combine_csv_files_with_liked_column(input_folder, output_file):
    """
    Combine all CSV files in the specified folder into a single CSV file
    and add a 'liked' column with a default value of 0.

    Args:
        input_folder (str): Path to the folder containing individual CSV files.
        output_file (str): Path to save the combined CSV file.
    """
    print(f"Combining CSV files from folder: {input_folder}")

    # List all files in the folder
    csv_files = [file for file in os.listdir(input_folder) if file.endswith('.csv')]

    # Initialize an empty list to hold the dataframes
    dataframes = []

    # Read each CSV file and append it to the list
    for file in csv_files:
        file_path = os.path.join(input_folder, file)
        print(f"Reading file: {file_path}")
        df = pd.read_csv(file_path)

        # Extract the coin name from the file name (remove "USDT" or other suffixes)
        coin_name = file.split('.')[0].replace("USDT", "").strip().upper()
        df['coin'] = coin_name  # Use the cleaned coin name

        # Add the 'liked' column with a default value of 0
        df['liked'] = 0

        dataframes.append(df)

    # Concatenate all dataframes into one
    combined_df = pd.concat(dataframes, ignore_index=True)

    # Save the combined dataframe to a single CSV file
    combined_df.to_csv(output_file, index=False)
    print(f"Combined CSV file saved to: {output_file}")


if __name__ == "__main__":
    # Specify the input folder and output file
    input_folder = "data"  # Folder where individual CSV files are stored
    output_file = "data/processed_data.csv"  # Output file path

    # Combine all CSV files and add the liked column
    combine_csv_files_with_liked_column(input_folder, output_file)
