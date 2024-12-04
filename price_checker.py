import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
import requests
import os
from email_credentials import SMTP_EMAIL, SMTP_PASSWORD  # Import email credentials from the separate file

TRACKED_COINS_FILE = "tracked_coins.csv"
NOTIFICATION_PREF_FILE = "notification_preferences.csv"

API_URL = "https://api.binance.com/api/v3/ticker/price"

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587


def send_email(to_email, subject, body):
    """Send an email notification."""
    try:
        msg = MIMEMultipart()
        msg["From"] = SMTP_EMAIL
        msg["To"] = to_email
        msg["Subject"] = subject

        # Email body
        msg.attach(MIMEText(body, "plain"))

        # Connect to the email server and send the email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.send_message(msg)

        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")


def load_tracked_coins():
    """Load the tracked coins data from the file."""
    if not os.path.exists(TRACKED_COINS_FILE):
        return pd.DataFrame(columns=["coin", "threshold", "initial_price"])
    return pd.read_csv(TRACKED_COINS_FILE)


def save_tracked_coins(data):
    """Save the updated tracked coins data back to the file."""
    data.to_csv(TRACKED_COINS_FILE, index=False)


def load_notification_preferences():
    """Load the user's notification preferences."""
    if not os.path.exists(NOTIFICATION_PREF_FILE):
        return {"email": ""}
    return pd.read_csv(NOTIFICATION_PREF_FILE).iloc[0].to_dict()


def fetch_coin_price(coin):
    """Fetch the current price of a coin from Binance API."""
    try:
        response = requests.get(API_URL, params={"symbol": f"{coin}USDT"})
        response.raise_for_status()
        data = response.json()
        return float(data["price"])
    except Exception as e:
        print(f"Failed to fetch price for {coin}: {e}")
        return None


def monitor_prices():
    """Monitor prices and send notifications when thresholds are met."""
    tracked_coins = load_tracked_coins()
    preferences = load_notification_preferences()

    if tracked_coins.empty:
        print("No coins are being tracked.")
        return

    if not preferences.get("email"):
        print("No email address configured for notifications.")
        return

    print("Checking prices...")

    coins_to_remove = []

    for _, row in tracked_coins.iterrows():
        coin = row["coin"]
        threshold = row["threshold"]
        initial_price = row["initial_price"]

        price = fetch_coin_price(coin)
        if price is None:
            continue

        # Calculate percentage change
        percentage_change = ((price - initial_price) / initial_price) * 100
        print(f"{coin}: Current price = {price}, Initial price = {initial_price}, Change = {percentage_change:.2f}%")

        if abs(percentage_change) >= threshold:
            direction = "increased" if percentage_change > 0 else "decreased"
            subject = f"Price Alert: {coin} has {direction} by {percentage_change:.2f}%"
            body = (
                f"The price of {coin} has {direction} by {percentage_change:.2f}%.\n"
                f"Initial price: {initial_price} USDT\n"
                f"Current price: {price} USDT\n"
                f"Threshold: {threshold}%"
            )
            send_email(preferences["email"], subject, body)

            # Mark the coin for removal after notification
            coins_to_remove.append(coin)

    # Remove notified coins from the tracking list
    if coins_to_remove:
        tracked_coins = tracked_coins[~tracked_coins["coin"].isin(coins_to_remove)]
        save_tracked_coins(tracked_coins)
        print(f"Removed the following coins from the tracking list: {', '.join(coins_to_remove)}")


if __name__ == "__main__":
    monitor_prices()
