import streamlit as st
from clients.mongodb_client import MongoDBClient
import requests
import os

# Configuration for Flask Auth Server
FLASK_AUTH_SERVER_URL = os.environ.get("FLASK_AUTH_SERVER_URL", "http://localhost:5000")

# Function to check if the user is authenticated
def check_authentication():
    try:
        # This is a simplified check. In a real app, you might check a session endpoint
        # or a specific cookie. For now, we assume if the Flask app redirects to Streamlit,
        # it has set a session. We'll rely on the Flask app to manage the session.
        # If the Streamlit app is accessed directly without a Flask session,
        # we'll redirect to the Flask login page.
        # This requires the Streamlit app to be served after Flask authentication.
        # For local development, we'll check if a 'username' is in session state (simulated).
        if 'username' not in st.session_state:
            # In a real deployment, Flask would handle the initial redirect.
            # For local testing, we can simulate a redirect if not authenticated.
            st.warning("You are not logged in. Redirecting to login page...")
            st.markdown(f'<meta http-equiv="refresh" content="0; url={FLASK_AUTH_SERVER_URL}/login">', unsafe_allow_html=True)
            st.stop()
        return True
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the authentication server. Please ensure it is running.")
        st.stop()
    except Exception as e:
        st.error(f"An error occurred during authentication check: {e}")
        st.stop()
    return False

# Perform authentication check
if check_authentication():
    st.set_page_config(page_title="Email Assistant", layout="wide")

    st.title("Email Assistant")

    st.sidebar.title("Navigation")
    st.sidebar.write("Future navigation options will go here.")

    # Initialize MongoDB Client
    mongo_client = MongoDBClient(base_url="http://localhost:8000") # Adjust URL if your MCP server is elsewhere

    st.write(f"Welcome, {st.session_state['username']}! Start chatting below.")

    # MongoDB Interaction Example
    st.subheader("MongoDB Interaction (Example)")
    with st.expander("Add/View Data in MongoDB"):
        new_data = st.text_input("Enter data to store in MongoDB:")
        if st.button("Add Data"):
            if new_data:
                result = mongo_client.insert_one("streamlit_data", {"value": new_data})
                if "error" in result:
                    st.error(f"Error adding data: {result['error']}")
                else:
                    st.success(f"Data added: {result}")
            else:
                st.warning("Please enter some data.")

        st.write("---")
        st.write("Current Data in 'streamlit_data' collection:")
        all_data = mongo_client.find_one("streamlit_data", {}) # A simple find_one to show any data
        if "error" in all_data:
            st.error(f"Error fetching data: {all_data['error']}")
        elif all_data:
            st.json(all_data)
        else:
            st.info("No data found yet.")


    # Chat interface placeholder
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What can I help you with?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            st.markdown("Hello! I'm your Email Assistant. How can I help you today?")