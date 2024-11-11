import streamlit as st
import random
import pandas as pd

# Function to generate a mock percentage change for analysis
def get_mock_percentage_change():
    return round(random.uniform(-10, 10), 2)

# Function to check if the criteria are met based on the threshold
def check_criteria(threshold, percentage_change):
    return percentage_change >= threshold

# Title and description for the app
st.title("Easy2Trade: Coin Tracking Interface")
st.write("Input your preferred coins, criteria, and tracking settings below.")

# Input fields for user data
# Define the list of available coins
available_coins = ["Bitcoin", "Ethereum", "Solana", "XRP", "Cardano"]

# Multi-select input for coins
coins = st.multiselect("Select coin(s) to track:", available_coins)
threshold = st.number_input("Enter percentage change threshold:", min_value=0.0, step=0.1)
interval = st.selectbox("Select the interval:", ["Minutes", "Hours", "Days"])
candlesticks = st.number_input("Enter number of candlesticks to look back:", min_value=1, step=1)

# Button to submit tracking criteria
if st.button("Add Tracking Criteria"):
    st.write("### Tracking Criteria Summary")
    st.write(f"Coins: {coins}")
    st.write(f"Percentage Change Threshold: {threshold}%")
    st.write(f"Interval: {interval}")
    st.write(f"Candlesticks to look back: {candlesticks}")

# Example of displaying tracked coins (temporary storage for demo)
if "tracked_coins" not in st.session_state:
    st.session_state["tracked_coins"] = []

# Add tracking info to session state
if st.button("Add to Tracked List"):
    st.session_state["tracked_coins"].append({
        "coins": coins,
        "threshold": threshold,
        "interval": interval,
        "candlesticks": candlesticks
    })
    st.success("Criteria successfully added to tracked list!")
st.write("### Analysis Results")

# Display analysis results for each tracked coin
for idx, criteria in enumerate(st.session_state["tracked_coins"]):
    st.write(f"**{idx + 1}. Coin(s): {', '.join(criteria['coins'])}**")
    
    # Generate a mock percentage change and check criteria
    percentage_change = get_mock_percentage_change()
    meets_criteria = check_criteria(criteria["threshold"], percentage_change)
    
    # Color-coded result
    color = "green" if meets_criteria else "red"
    criteria_text = "Criteria Met" if meets_criteria else "Criteria Not Met"
    
    # Display criteria status and percentage change
    st.markdown(f"**Status:** <span style='color:{color}'>{criteria_text}</span>", unsafe_allow_html=True)
    st.write(f"**Percentage Change:** {percentage_change}% (Threshold: {criteria['threshold']}%)")
    st.write("—" * 20)

st.write("### Currently Tracked Coins")

for idx, criteria in enumerate(st.session_state["tracked_coins"]):
    st.write(f"**{idx + 1}. Coin(s): {', '.join(criteria['coins'])}**")
    st.write(f"Threshold: {criteria['threshold']}%")
    st.write(f"Interval: {criteria['interval']}")
    st.write(f"Candlesticks: {criteria['candlesticks']}")

    # Edit and delete buttons
    if st.button(f"Edit Entry {idx + 1}", key=f"edit_{idx}"):
        st.session_state["edit_index"] = idx  # Save the index of the entry to edit
    if st.button(f"Remove Entry {idx + 1}", key=f"remove_{idx}"):
        st.session_state["tracked_coins"].pop(idx)
        st.experimental_rerun()  # Refresh to show updated list
    st.write("—" * 20)

# Display editable fields if an entry is selected for editing
if "edit_index" in st.session_state:
    edit_index = st.session_state["edit_index"]
    st.write("### Edit Tracked Entry")

    # Pre-fill fields with existing data
    edit_coins = st.multiselect("Select coin(s) to track:", available_coins, default=st.session_state["tracked_coins"][edit_index]["coins"])
    edit_threshold = st.number_input("Enter percentage change threshold:", min_value=0.0, step=0.1, value=st.session_state["tracked_coins"][edit_index]["threshold"])
    edit_interval = st.selectbox("Select the interval:", ["Minutes", "Hours", "Days"], index=["Minutes", "Hours", "Days"].index(st.session_state["tracked_coins"][edit_index]["interval"]))
    edit_candlesticks = st.number_input("Enter number of candlesticks to look back:", min_value=1, step=1, value=st.session_state["tracked_coins"][edit_index]["candlesticks"])

    # Button to save changes
    if st.button("Save Changes"):
        # Update the entry in session state
        st.session_state["tracked_coins"][edit_index] = {
            "coins": edit_coins,
            "threshold": edit_threshold,
            "interval": edit_interval,
            "candlesticks": edit_candlesticks
        }
        del st.session_state["edit_index"]  # Exit edit mode
        st.success("Entry updated successfully!")
        st.experimental_rerun()

# Display currently tracked coins
st.write("### Currently Tracked Coins")
for idx, criteria in enumerate(st.session_state["tracked_coins"]):
    st.write(f"{idx + 1}. Coins: {criteria['coins']}, Threshold: {criteria['threshold']}%, Interval: {criteria['interval']}, Candlesticks: {criteria['candlesticks']}")
