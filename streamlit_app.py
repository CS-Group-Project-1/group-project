import streamlit as st
from landing_page import show_landing_page
from coin_search import show_coin_search
from feedback_and_recommendations import show_feedback_page

# Initialize session state for navigation
if "page" not in st.session_state:
    st.session_state["page"] = "landing_page"

# Sidebar navigation
st.sidebar.title("Navigation")
navigation = st.sidebar.radio(
    "Go to:",
    ["Landing Page", "Coin Search", "Feedback & Recommendations"]
)

# Set session state based on navigation
if navigation == "Landing Page":
    st.session_state["page"] = "landing_page"
elif navigation == "Coin Search":
    st.session_state["page"] = "coin_search"
elif navigation == "Feedback & Recommendations":
    st.session_state["page"] = "feedback"

# Render the selected page
if st.session_state["page"] == "landing_page":
    show_landing_page()
elif st.session_state["page"] == "coin_search":
    show_coin_search()
elif st.session_state["page"] == "feedback":
    show_feedback_page()
