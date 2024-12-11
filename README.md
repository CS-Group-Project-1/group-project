# group-project

Welcome to Easy2Trade, developed for our CS group project!

Here is a brief overview of the content of the different files that are part of our project/appplication:

-app.py: THIS IS THE FILE THAT NEEDS TO BE RUN IN ORDER TO RUN THE APPLICATION! 

-coin_search.py: this file contains the building pieces for the COIN SEARCH page of the application; 
specifically, the user can input a coin, an interval for the analysis, as well as the percentage threshold; there are buttons to add/remove coins as well as to kickstart the analysis. A candlestick graph is also displayed. Finally, the page includes buttons to like / dislike a coin (which is relevant in relation to our machine learning approach)

-combine_csv.py: as it can be understood from the name, the main goal of this file is combining the different CSV files that we have in the "data" folder into a single CSV file. Additionally, in the combined dataframe we add a column named "liked" that has a default value of 0. This column is relevant in relation to the user's feedback (i.e., the user's likes and dislikes), which is on turn crucial for our machine learning approach

-data_fetcher.py: file dedicated to fetching the historical data for the coins from the Binance API, like for example the price of the coins, the trading volume, and so on. The data is fetched to a determined and predefined list of symbols. The file also implements the processing of the fetched data in order to calculate metrics such as volatility, average volume, and trend of the trades; these calculations are then saved into a CSV file. The CSV files are further updated with the categorization of volatility and average volume into categories (low, medium, high).

-email_credentials.py: this file contains the credentials necessary for the implementation of the email notification system. More explanations on the nature and characteristics of this file follow below.

-feedback_and_recommendations.py: contains the building pieces for the app's FEEDBACK AND RECOMMENDATIONS page. We implement crucial elements for the management of the user's feedback, such as buttons that allow the user to remove the coin from the liked / disliked coins. Crucially,
the user can also see the feedback given to the coins, i.e. the liked and disliked coins are displayed.Additionally, this page also shows the coins that the user might like based on their expressed preference, i.e. it shows the recommendations for coins generated based on the feedback given by the user. Further elements handled in this script relate principally to data synchronization.

-feedback_updater.py: dedicated to the definition of a function that enables to update the feedback column, i.e. the 'liked' column, for a specific coin in the dataset.

-landing_page.py: contains elements of the LANDING PAGE of the app, different sections explain a variety of aspects of the app, like to illustrate the overall goal and functionality, an explanation of what a candlestick chart is for users that are not very familiar with trading, a brief explanation of the app's machine learning approach alongside the supported coins and some limitations.

-ml_model.py: file containing the machine learning (ml) model. The machine learning approach that we chose for our project entails the generation of recommendations for coins that the user might like based on the feedback, so on the likes/dislikes, that the user gave to other coins.

-price_checker.py: this file is relevant in relation to the tracked_coins_page.py file explained below.
In brief, it tackles the functionality that allows to send an email when the specified percentage threshold is met; it additionally fetches data from the Binance API in order to be able to monitor the prices and send a notification when the specified percentage threshold is met.

-recommendation_section.py: contains crucial functions needed to display the recommendation section; the elements defined in this file will then be the crucial building pieces of the FEEDBACK AND RECOMMENDATIONS page explained above.

-tracked_coins_page.py: contains the elements for the TRACKED COINS & NOTIFICATION page of the app; the user will be able to manage the tracked coins and the email notification preferences. The email functionality of the app entails, as briefly mentioned before, sending an email notification to the user when the specific percentage threshold is met. IMPORTANT OBSERVATION: during the testing of the application, we noticed that the email notifications sometimes ended in the spam of the user; i.e., the spam folder might have to be checked.

-utils.py: contains various functions that we classified as utils; these functions complete a specific task that is then needed in other parts of the scripts/files. In detail, the file contains a function that interacts with the Binance API in order to fetch the data about the historical prices of coins, another function that calculates the percentage change in the price of coins, and finally a function that allows us to create the candlestick graph for the coin in question (to create the graph, we use the plotly library).

Apart from the py files, the project also contains other files essential for the application to work, entailing:
-candlestick_example.jgp: example image used in the landing page to explain the nature of a candlestick graph;
-notification_preferences.csv and tracked_coins.csv: files containing the data regarding the tracked coins and the user's notification preferences;
-trained_model.pkl: file relevant for the saving of the trained ml model
-data folder: contains the csv files of the different types of coins, relevant in different steps of the app;
-gitignore: in order to prevent the exposition of sensitive email data

Additionally, the project's zip naturally also contains, as per the project guidelines, the video and the contribution matrix.


LIST OF SUPPLEMENTARY AIDS

In the code:
-ChatGPT: we used this tool in different parts of the code and in a variety of ways. The specific usage
of ChatGPT is documented in extreme detail in all the lines of code concerned.

In the video:
-ChatGPT: used to generate the featured images
-ElevenLabs: used to generate the voices
-Premiere Pro: used for the editing



EMAIL NOTIFICATIONS AND CREDENTIALS

The following paragraphs explain the process that the user would have to follow in order to set up the
notification system. However, for the scope of our project we already created the file
email_credentials.py and inserted there an email address created specifically for the project with the
correlated password. Thus, the following paragraphs are here for an informative scope, but 
the process explained DOES NOT HAVE TO BE EXECUTED AGAIN.


Setting Up Email Notifications; ONLY FOR INFORMATIVE PURPOSES, THIS PROCESS DOES NOT HAVE TO BE EXECUTED AGAIN

This project uses Gmail to send email notifications when tracked coin prices meet the specified thresholds. To ensure the system works correctly, the user will need to create an email_credentials.py file and configure Gmail to generate an app-specific password. The necessary steps to setup the email notifications system are the following:

STEP 1: Create the email_credentials.py File
In the root directory of the project, create a new Python file named email_credentials.py.
Add the following code to the file and replace the placeholders with your Gmail address and the generated app password:

SMTP_EMAIL = "your_email@gmail.com"  # Replace with your Gmail address
SMTP_PASSWORD = "your_app_password"  # Later, replace with the app password from Google (generated according to the steps explained below)

Important: Do not commit this file to version control. Make sure it's added to your .gitignore file to prevent exposing your credentials.

STEP 2: Generate an App Password in Gmail
To ensure secure access, Gmail requires an app-specific password for third-party applications. You can generate one by doing the following:

Enable 2-Step Verification:
Go to Google My Account Security.
Scroll down to "Signing in to Google" and enable 2-Step Verification if it's not already enabled.

Generate an App Password:
After having enabled 2-Step Verification, return to the Security page in your Google account.
Scroll to "Signing in to Google" and select App Passwords.
Under "Select the app and device you want to generate the app password for," choose:
-App: Select Mail.
-Device: Select your device or choose Other (Custom name) and type a name like Coin Tracker.
-Click Generate.
-Google will display a 16-character app password. Copy this password.
-Update the email_credentials.py File:
Replace "your_app_password" in the email_credentials.py file with the generated app password.


STEP 3: Verify the Setup
Follow this step in case there's a need to ensure that the email_credentials.py file is properly configured with your Gmail address and app password.
Run the application and add a coin to track with a threshold.
Trigger the "Run Price Check Now" button in the application's tracked coins page to test if notifications are sent to the specified email.
 
 Finally, we briefly address some possible errors that could arise. Namely, we shortly focus on troubleshooting:
-SMTP Authentication Error: Ensure the Gmail address and app password in email_credentials.py are correct.
-App Password Not Available: Make sure 2-Step Verification is enabled for your Google account.
-Email Not Received: Check your spam/junk folder or ensure the recipient email is correct.
