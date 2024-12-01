import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle
import os

class MLModel:
    def __init__(self, data_path, model_path="trained_model.pkl"):
        self.data_path = data_path
        self.model_path = model_path
        self.model = None

    def load_data(self):
        """
        Load the dataset from the specified path.
        """
        print("Loading dataset...")
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Dataset not found at {self.data_path}. Please check the file path.")
        data = pd.read_csv(self.data_path)
        return data

    def preprocess_data(self):
        """
        Preprocess the data for training and testing.
        """
        print("Loading and preprocessing data...")

        # Load the dataset
        data = self.load_data()

        # Ensure there are no missing values in the 'trend' column
        if "trend" not in data.columns or data["trend"].isnull().any():
            print("Fixing missing or invalid 'trend' values...")
            data["trend"] = data["trend"].fillna("Stable")  # Fill missing values with a default

        # Specify features and target
        features = ["volatility", "avg_volume", "volatility_category", "avg_volume_category"]
        target = "liked"

        # Drop rows with missing values in features or target
        data = data.dropna(subset=features + [target])

        # Encode categorical features
        data = pd.get_dummies(data, columns=["volatility_category", "avg_volume_category", "trend"], drop_first=True)

        # Separate features (X) and target (y)
        X = data.drop(columns=["liked", "coin", "timestamp", "close", "volume"])  # Exclude non-predictive columns
        y = data["liked"]

        return X, y

    def train_model(self):
        """
        Train the Random Forest model.
        """
        print("Splitting data into training and test sets...")
        X, y = self.preprocess_data()
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        print("Training the model...")
        self.model = RandomForestClassifier(random_state=42)
        self.model.fit(X_train, y_train)

        print("Evaluating the model...")
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Model accuracy: {accuracy * 100:.2f}%")

        # Save the trained model
        with open(self.model_path, "wb") as file:
            pickle.dump(self.model, file)
        print(f"Trained model saved to {self.model_path}.")

    def recommend_coins(self, user_feedback):
        """
        Generate recommendations based on user feedback.
        :param user_feedback: List of liked coins by the user.
        :return: List of recommended coins.
        """
        print("Generating recommendations...")
        if not self.model:
            if os.path.exists(self.model_path):
                with open(self.model_path, "rb") as file:
                    self.model = pickle.load(file)
            else:
                raise FileNotFoundError("Trained model not found. Please train the model first.")

        # Simulate user feedback as input features for prediction
        feedback_data = self.load_data()
        feedback_data = feedback_data[feedback_data["coin"].isin(user_feedback)]

        if feedback_data.empty:
            print("No user feedback found in the dataset.")
            return []

        feedback_features = feedback_data.drop(columns=["liked", "coin", "timestamp", "close", "volume"])
        feedback_features = pd.get_dummies(feedback_features, columns=["volatility_category", "avg_volume_category", "trend"], drop_first=True)

        # Align features with the model's training data
        trained_features = self.model.feature_names_in_
        feedback_features = feedback_features.reindex(columns=trained_features, fill_value=0)

        predictions = self.model.predict_proba(feedback_features)[:, 1]
        feedback_data["score"] = predictions

        recommended_coins = feedback_data.sort_values(by="score", ascending=False)["coin"].tolist()
        print(f"Recommended coins: {recommended_coins[:5]}")
        return recommended_coins[:5]


# Main script to train and test the model
if __name__ == "__main__":
    ml_model = MLModel(data_path="data/processed_data.csv")
    ml_model.train_model()
