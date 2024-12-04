# group-project
Setting Up Email Notifications
This project uses Gmail to send email notifications when tracked coin prices meet the specified thresholds. To ensure the system works correctly, you'll need to create an email_credentials.py file and configure Gmail to generate an app-specific password. Follow these steps:

Step 1: Create the email_credentials.py File
In the root directory of the project, create a new Python file named email_credentials.py.
Add the following code to the file and replace the placeholders with your Gmail address and the generated app password:

SMTP_EMAIL = "your_email@gmail.com"  # Replace with your Gmail address
SMTP_PASSWORD = "your_app_password"  # Replace with the app password from Google

Important: Do not commit this file to version control. Make sure it's added to your .gitignore file to prevent exposing your credentials.

Step 2: Generate an App Password in Gmail
To ensure secure access, Gmail requires an app-specific password for third-party applications. Follow these steps to generate one:

Enable 2-Step Verification:

Go to Google My Account Security.
Scroll down to "Signing in to Google" and enable 2-Step Verification if it's not already enabled.
Generate an App Password:

After enabling 2-Step Verification, return to the Security page in your Google account.
Scroll to "Signing in to Google" and select App Passwords.
Under "Select the app and device you want to generate the app password for," choose:
App: Select Mail.
Device: Select your device or choose Other (Custom name) and type a name like Coin Tracker.
Click Generate.
Google will display a 16-character app password. Copy this password.
Update the email_credentials.py File:

Replace "your_app_password" in the email_credentials.py file with the generated app password.

Step 3: Verify the Setup
Ensure that the email_credentials.py file is properly configured with your Gmail address and app password.
Run the application and add a coin to track with a threshold.
Trigger the "Run Price Check Now" button to test if notifications are sent to the specified email.
Troubleshooting
SMTP Authentication Error: Ensure the Gmail address and app password in email_credentials.py are correct.
App Password Not Available: Make sure 2-Step Verification is enabled for your Google account.
Email Not Received: Check your spam/junk folder or ensure the recipient email is correct.
By following these steps, you should have a fully functional email notification system integrated into your application. Let me know if additional clarification is needed!