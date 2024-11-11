import streamlit as st
import random
import pandas as pd
import matplotlib.pyplot as plt

# Function to generate a mock percentage change for analysis
def get_mock_percentage_change():
    return round(random.uniform(-10, 10), 2)

# Function to check if the criteria are met based on the threshold
def check_criteria(threshold, percentage_change):
    return percentage_change >= threshold

# Title and description for the app
st.title("🚀 Easy2Trade: Coin Tracking Interface")
st.write("Track your favorite cryptocurrencies, set custom alerts, and analyze market trends.")

# Divider for section
st.markdown("---")

# Define the list of available coins
available_coins = ["Bitcoin", "Ethereum", "Solana", "XRP", "Cardano"]

# Use columns for a more compact input section
st.header("🔍 Set Tracking Criteria")
col1, col2 = st.columns(2)

# Coin selection and percentage change threshold
coins = col1.multiselect("Select coin(s) to track:", available_coins)
threshold = col2.number_input("Percentage change threshold (%):", min_value=0.0, step=0.1)

# Interval and candlesticks
interval = col1.selectbox("Select the interval:", ["Minutes", "Hours", "Days"])
candlesticks = col2.number_input("Number of candlesticks to look back:", min_value=1, step=1)

# Divider for section
st.markdown("---")

# Add some empty space
st.write(" ")

# Initialize session state for tracked coins if not already set
if "tracked_coins" not in st.session_state:
    st.session_state["tracked_coins"] = []

# Button to add criteria to the tracked list with success message
if coins and st.button("Add to Tracked List"):
    st.session_state["tracked_coins"].append({
        "coins": coins,
        "threshold": threshold,
        "interval": interval,
        "candlesticks": candlesticks
    })
    st.success("Criteria successfully added to tracked list! 🎉")

# Divider for section
st.markdown("---")

# Analysis Results Section
st.header("📈 Analysis Results")

for idx, criteria in enumerate(st.session_state["tracked_coins"]):
    st.subheader(f"{idx + 1}. {', '.join(criteria['coins'])}")
    
    # Mock data for demonstration: Generate a percentage change and check if criteria are met
    percentage_change = get_mock_percentage_change()
    meets_criteria = check_criteria(criteria["threshold"], percentage_change)
    
    # Display status with color-coding
    color = "green" if meets_criteria else "red"
    criteria_text = "✅ Criteria Met" if meets_criteria else "❌ Criteria Not Met"
    
    st.markdown(f"**Status:** <span style='color:{color}'>{criteria_text}</span>", unsafe_allow_html=True)
    st.write(f"**Percentage Change:** {percentage_change}% (Threshold: {criteria['threshold']}%)")
    
    # Generate a simple line chart for trend visualization
    st.write("Price Trend (Mock Data)")
    trend_data = pd.DataFrame([random.uniform(-5, 5) for _ in range(10)], columns=["Price Change"])
    st.line_chart(trend_data)
    
    # Add horizontal divider
    st.markdown("---")

# Interactive Management Section
st.header("🛠 Manage Tracked Coins")

# Display tracked coins with edit and delete options
for idx, criteria in enumerate(st.session_state["tracked_coins"]):
    st.subheader(f"{idx + 1}. {', '.join(criteria['coins'])}")
    st.write(f"Threshold: {criteria['threshold']}%")
    st.write(f"Interval: {criteria['interval']}")
    st.write(f"Candlesticks: {criteria['candlesticks']}")

    # Add edit and delete buttons for each entry
    if st.button(f"Edit Entry {idx + 1}", key=f"edit_{idx}"):
        st.session_state["edit_index"] = idx  # Save index of entry to edit
    if st.button(f"Remove Entry {idx + 1}", key=f"remove_{idx}"):
        st.session_state["tracked_coins"].pop(idx)
        st.experimental_rerun()  # Refresh to show updated list
    st.write("—" * 20)

# Editable fields if in edit mode
if "edit_index" in st.session_state:
    edit_index = st.session_state["edit_index"]
    st.write("### Edit Tracked Entry")

    # Pre-fill fields with current data
    edit_coins = st.multiselect("Select coin(s) to track:", available_coins, default=st.session_state["tracked_coins"][edit_index]["coins"])
    edit_threshold = st.number_input("Percentage change threshold (%):", min_value=0.0, step=0.1, value=st.session_state["tracked_coins"][edit_index]["threshold"])
    edit_interval = st.selectbox("Select the interval:", ["Minutes", "Hours", "Days"], index=["Minutes", "Hours", "Days"].index(st.session_state["tracked_coins"][edit_index]["interval"]))
    edit_candlesticks = st.number_input("Number of candlesticks to look back:", min_value=1, step=1, value=st.session_state["tracked_coins"][edit_index]["candlesticks"])

    # Save changes button
    if st.button("Save Changes"):
        st.session_state["tracked_coins"][edit_index] = {
            "coins": edit_coins,
            "threshold": edit_threshold,
            "interval": edit_interval,
            "candlesticks": edit_candlesticks
        }
        del st.session_state["edit_index"]  # Exit edit mode
        st.success("Entry updated successfully! 🎉")
        st.experimental_rerun()
