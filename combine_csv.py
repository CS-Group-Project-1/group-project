import os
import pandas as pd


#The present file has the main goal of combining the different CSV files that we have in the "data" folder
#into a single CSV file. Additionally, in the combined dataframe we add a column named "liked" that 
#has a default value of 0. This column is relevant in relation to the user's feedback (i.e., the user's
#likes and dislikes), which is on turn crucial for our machine learning approach

#we define the function that will combine all the CSV files in one as illustrated in the introductive paragraph
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

    # Apply read_csv to each CSV file, thus creating a dataframe, and then append it to the list
    for file in csv_files:
        file_path = os.path.join(input_folder, file) #to optimally join the components of the path
        print(f"Reading file: {file_path}")
        df = pd.read_csv(file_path)

        # Extract the coin name from the file name (remove "USDT" or other suffixes)
        coin_name = file.split('.')[0].replace("USDT", "").strip().upper()
        df['coin'] = coin_name  # Use the cleaned coin name
        #process of cleaning the coin name in detail: we split the string file after the period,
        #removing the '.csv' extension. Then, we want to get rid of the USDT part, and this time
        #we approach this  by replacing it with an empty string. We then remove white spaces at 
        #the beginning or the end of the string and convert it all to uppercases

        # Add the 'liked' column with a default value of 0 to the dataframe
        df['liked'] = 0

        dataframes.append(df) #we append the created data frame to the initialized empty dataframe list

    #Concatenate all dataframes into one
    combined_df = pd.concat(dataframes, ignore_index=True)

    #Finally, save the combined dataframe into a single CSV file
    combined_df.to_csv(output_file, index=False)
    print(f"Combined CSV file saved to: {output_file}")

#we ensure that the code is executed as a main program 
if __name__ == "__main__":
    # Specify the input folder and output file
    input_folder = "data"  # Folder where individual CSV files are stored
    output_file = "data/processed_data.csv"  # Output file path

    # Combine all CSV files and add the liked column
    combine_csv_files_with_liked_column(input_folder, output_file)
