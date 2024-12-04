import streamlit as st
import pandas as pd
import os
import requests

# Paths for saving tracked coins and user preferences
TRACKED_COINS_FILE = "tracked_coins.csv"
NOTIFICATION_PREF_FILE = "notification_preferences.csv"


def fetch_binance_symbols():
    """
    Fetches the list of supported symbols from Binance API.
    Returns a list of valid coin symbols.
    """
    try:
        response = requests.get("https://api.binance.com/api/v3/exchangeInfo")
        response.raise_for_status()
        data = response.json()
        symbols = [symbol["symbol"][:-4] for symbol in data["symbols"] if symbol["symbol"].endswith("USDT")]
        return list(set(symbols))
    except Exception:
        st.error("Failed to fetch Binance symbols. Please try again later.")
        return []


def load_tracked_coins():
    """Load the tracked coins data from the file."""
    if os.path.exists(TRACKED_COINS_FILE):
        return pd.read_csv(TRACKED_COINS_FILE)
    else:
        return pd.DataFrame(columns=["coin", "threshold"])


def save_tracked_coins(data):
    """Save the tracked coins data to the file."""
    data.to_csv(TRACKED_COINS_FILE, index=False)


def load_notification_preferences():
    """Load the user's notification preferences."""
    if os.path.exists(NOTIFICATION_PREF_FILE):
        return pd.read_csv(NOTIFICATION_PREF_FILE).iloc[0]
    else:
        return {"email": "", "phone": ""}


def save_notification_preferences(email, phone):
    """Save the user's notification preferences."""
    pd.DataFrame([{"email": email, "phone": phone}]).to_csv(NOTIFICATION_PREF_FILE, index=False)


def show_tracked_coins_page():
    """
    Displays the Tracked Coins page.
    Allows users to manage tracked coins and update notification preferences.
    """
    st.title("Tracked Coins & Notifications")

    # Fetch Binance-supported symbols
    if "binance_symbols" not in st.session_state:
        st.session_state["binance_symbols"] = fetch_binance_symbols()

    # Load tracked coins
    if "tracked_coins" not in st.session_state:
        st.session_state["tracked_coins"] = load_tracked_coins()

    tracked_coins = st.session_state["tracked_coins"].copy()  # Copy to detect changes

    # Load user notification preferences
    preferences = load_notification_preferences()
    email = preferences.get("email", "")
    phone = preferences.get("phone", "")

    # Section 1: Tracked Coins
    st.subheader("Tracked Coins")

    # Persistent success message display
    if "success_message" in st.session_state and st.session_state["success_message"]:
        st.success(st.session_state["success_message"])
        st.session_state["success_message"] = None  # Clear the message after displaying

    changes_made = False  # Track if any changes are made

    if not tracked_coins.empty:
        for index, row in tracked_coins.iterrows():
            col1, col2, col3 = st.columns([6, 3, 1])
            col1.write(f"**{row['coin']}** (Threshold: {row['threshold']}%)")
            new_threshold = col2.number_input(
                f"Set new threshold for {row['coin']}",
                min_value=0.1,  # Prevent user from entering 0
                value=row["threshold"],
                key=f"threshold_{index}",
            )
            if new_threshold != row["threshold"]:
                tracked_coins.at[index, "threshold"] = new_threshold
                changes_made = True
            if col3.button("❌ Remove", key=f"remove_{index}"):
                tracked_coins = tracked_coins.drop(index)
                save_tracked_coins(tracked_coins)
                st.session_state["tracked_coins"] = tracked_coins
                st.session_state["success_message"] = f"{row['coin']} removed from the tracking list."
                st.rerun()
    else:
        st.info("No coins are currently being tracked.")

    # Add an "Apply Changes" button
    apply_button = st.button("Apply Changes")

    if apply_button:
        # Check if the dataframe has been modified
        if changes_made:
            save_tracked_coins(tracked_coins)
            st.session_state["tracked_coins"] = tracked_coins
            st.session_state["tracked_coins_message"] = ("success", "Changes applied successfully!")
            st.rerun()  # Refresh the page
        else:
            st.session_state["tracked_coins_message"] = ("info", "No changes were made.")
            st.rerun()  # Refresh the page

    # Display message below the button
    if "tracked_coins_message" in st.session_state:
        message_type, message_text = st.session_state["tracked_coins_message"]
        if message_type == "success":
            st.success(message_text)
        elif message_type == "info":
            st.info(message_text)
        # Clear the message after displaying it
        del st.session_state["tracked_coins_message"]


    # Add new coin to track
    st.subheader("Add a Coin to Track")
    new_coin = st.text_input("Enter coin symbol (e.g., BTC, ETH):").strip().upper()
    new_threshold = st.number_input("Enter threshold (%)", min_value=0.1, step=0.1, value=1.0)  # Prevent 0
    if st.button("Add Coin to Track"):
        if not new_coin:
            st.error("Please enter a valid coin symbol.")
        elif new_coin not in st.session_state["binance_symbols"]:
            st.error(f"{new_coin} is not a valid Binance-supported symbol.")
        elif new_coin in tracked_coins["coin"].values:
            st.warning(f"{new_coin} is already being tracked.")
        else:
            new_row = pd.DataFrame({"coin": [new_coin], "threshold": [new_threshold]})
            tracked_coins = pd.concat([tracked_coins, new_row], ignore_index=True)
            save_tracked_coins(tracked_coins)
            st.session_state["tracked_coins"] = tracked_coins
            st.session_state["success_message"] = f"{new_coin} has been added to the tracked coins list."
            st.rerun()

    # Section 2: Notification Preferences
    st.subheader("Notification Preferences")
    st.write("Set how you would like to be notified when thresholds are met.")

    updated_email = st.text_input("Email Address", value=email, placeholder="Enter your email address")
    updated_phone = st.text_input("Phone Number", value=phone, placeholder="Enter your phone number (optional)")

    if st.button("Update Preferences"):
        if not updated_email and not updated_phone:
            st.error("Please provide at least one contact method (email or phone).")
        else:
            save_notification_preferences(updated_email, updated_phone)
            st.session_state["success_message"] = "Notification preferences updated successfully!"
            st.rerun()

    st.markdown("---")
    st.caption("You will be notified when a tracked coin crosses the specified threshold.")
