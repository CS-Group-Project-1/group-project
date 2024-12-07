import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle
import os

#This file contains the machine learning (ML) model. We define the class 'MLModel' and the relevant methods
#The functions that are then defined include two functions that respectively load and reprocess the data,
#a function that implements the training of the ML model, and one that generates the recommendations for the coins.


#the first step is defining the MLModel class
class MLModel:
    def __init__(self, data_path, model_path="trained_model.pkl"):
        self.data_path = data_path #path to input the dataset
        self.model_path = model_path #path to save the trained model
        self.model = None #placeholder for the model instance

    #as documented in the docstring, the following function will load the dataset from the path that we specify
    def load_data(self):
        """
        Load the dataset from the specified path.
        """
        print("Loading dataset...")
        if not os.path.exists(self.data_path): #we check if the file exists; if it does not exist, the next line raises an error
            raise FileNotFoundError(f"Dataset not found at {self.data_path}. Please check the file path.")
        data = pd.read_csv(self.data_path) #we read the csv data into a dataframe
        return data

    #this function prepares, i.e. preprocesses, the data in order to be able to use it for training and testing
    def preprocess_data(self):
        """
        Preprocess the data for training and testing.
        """
        print("Loading and preprocessing data...")

        # Load the dataset by using the function defined above
        data = self.load_data()

        # Ensure there are no missing values in the 'trend' column
        if "trend" not in data.columns or data["trend"].isnull().any():
            print("Fixing missing or invalid 'trend' values...")
            data["trend"] = data["trend"].fillna("Stable")  # Fill the missing values with a default (if there's any)

        # Specify features and target columns
        features = ["volatility", "avg_volume", "volatility_category", "avg_volume_category"]
        target = "liked"

        # Drop rows with missing values in features or target
        data = data.dropna(subset=features + [target])

        # Encode categorical features
        data = pd.get_dummies(data, columns=["volatility_category", "avg_volume_category", "trend"], drop_first=True)

        # Separate features (X) and target (y); 
        # OBSERVATION: we asked ChatGPT insights on how to split the dataset into training and testing sets
        # we then adapted the general case that we got to the characteristics of our specific data
        X = data.drop(columns=["liked", "coin", "timestamp", "close", "volume"])  # Exclude non-predictive columns
        y = data["liked"]

        return X, y

    #we define a function that will implement the training of the model
    def train_model(self):
        """
        Train the Random Forest model.
        """
        print("Splitting data into training and test sets...")
        X, y = self.preprocess_data() #we preprocess the data with the function defined above
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        #OBSERVATION: in relation to the OBSERVATION a few lines above, the insights we got from ChatGPT
        #to split the data apply here too. However, in the present case we decided to keep the result that was given from ChatGPT.

        print("Training the model...")
        #the following lines were created taking inspiration from ChatGPT; we gathered 
        #valuable insights and then we came up with the solution for our case
        self.model = RandomForestClassifier(random_state=42) #Initialization of the classifier
        self.model.fit(X_train, y_train) #use the training data to train the model

        print("Evaluating the model...")
        y_pred = self.model.predict(X_test) #make predictions on the test set
        accuracy = accuracy_score(y_test, y_pred) #calculation of accuracy score by using the appropriate function from sklearn module
        print(f"Model accuracy: {accuracy * 100:.2f}%")

        # Save the trained model in a file;
        with open(self.model_path, "wb") as file:
            pickle.dump(self.model, file)
        print(f"Trained model saved to {self.model_path}.")

    #as documented in the docstring, the following function generates the recommendations based on the 
    #user's feedback; i.e., it wil predict which coins (for which a feedback was not given) 
    #the user might like depending on the given feedback
    def recommend_coins(self, user_feedback):
        """
        Generate recommendations based on user feedback.
        :param user_feedback: List of liked coins by the user.
        :return: List of recommended coins.
        """
        print("Generating recommendations...")
        if not self.model: #we check if the model is loaded
            if os.path.exists(self.model_path):
                with open(self.model_path, "rb") as file:
                    self.model = pickle.load(file) #we load the trained model
            else:
                raise FileNotFoundError("Trained model not found. Please train the model first.") 

        # We load the data
        data = self.load_data()

        # Separate liked, disliked, and unrated coins
        liked_coins = data[data["coin"].isin(user_feedback) & (data["liked"] > 0)]
        unrated_coins = data[data["liked"] == 0]

        if liked_coins.empty or unrated_coins.empty:
            print("No recommendations possible due to insufficient data.")
            return []

        # Preprocess features for prediction
        unrated_features = unrated_coins.drop(columns=["liked", "coin", "timestamp", "close", "volume"])
        unrated_features = pd.get_dummies(unrated_features, columns=["volatility_category", "avg_volume_category", "trend"], drop_first=True)

        # Align columns with the training data
        trained_features = self.model.feature_names_in_
        unrated_features = unrated_features.reindex(columns=trained_features, fill_value=0)

        # Predict probabilities for unrated coins; OBSERVATION: approach for the next lines was inspired by ChatGPT and integrated into the script by making various adjustments
        unrated_coins["recommendation_score"] = self.model.predict_proba(unrated_features)[:, 1]

        # Sort by recommendation score and filter out already-liked coins
        recommended_coins = (
            unrated_coins.sort_values(by="recommendation_score", ascending=False)["coin"]
            .drop_duplicates()
            .tolist()
        )
        print(f"Recommended coins: {recommended_coins[:5]}")

        return recommended_coins[:5]


# Main script to train and test the model (as in the case of other scripts, with the first line of the 
# next code snippet we ensure that the code below is executed only if the script is run directly/as a main program)
if __name__ == "__main__":
    ml_model = MLModel(data_path="data/processed_data.csv")
    ml_model.train_model()
