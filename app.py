import streamlit as st
from landing_page import show_landing_page #import function that displays the landing page
from coin_search import show_coin_search #import function that displays the coin search page
from feedback_and_recommendations import show_feedback_page #import function that displays the feedback page
from tracked_coins_page import show_tracked_coins_page  #import the new tracked coins page

#THIS IS THE SCRIPT THAT NEEDS TO BE RUN IN ORDER TO BE ABLE TO RUN THE APPLICATION

# Initialize session state for navigation
if "page" not in st.session_state:
    st.session_state["page"] = "landing_page"

# Sidebar navigation
st.sidebar.title("Navigation")
navigation = st.sidebar.radio(
    "Go to:",
    ["Landing Page", "Coin Search", "Feedback & Recommendations", "Tracked Coins"]  #add "Tracked Coins"
)

# Set session state based on navigation
if navigation == "Landing Page": #add navigation for "Landing Page"
    st.session_state["page"] = "landing_page"
elif navigation == "Coin Search": #add navigation for "Coin Search"
    st.session_state["page"] = "coin_search"
elif navigation == "Feedback & Recommendations": #add navigation for "Feedback and recommendations"
    st.session_state["page"] = "feedback"
elif navigation == "Tracked Coins":  #add navigation for "Tracked Coins"
    st.session_state["page"] = "tracked_coins"

# Render the selected page
if st.session_state["page"] == "landing_page":
    show_landing_page()
elif st.session_state["page"] == "coin_search":
    show_coin_search()
elif st.session_state["page"] == "feedback":
    show_feedback_page()
elif st.session_state["page"] == "tracked_coins":  # Render the new tracked coins page
    show_tracked_coins_page()
