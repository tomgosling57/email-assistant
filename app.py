import streamlit as st
import os
from dotenv import load_dotenv

def save_credentials(qdrant_api_key, email_api_key, scrapeless_api_key):
    with open(".env", "w") as f:
        f.write(f"QDRANT_API_KEY={qdrant_api_key}\n")
        f.write(f"EMAIL_API_KEY={email_api_key}\n")
        f.write(f"SCRAPELESS_API_KEY={scrapeless_api_key}\n")
    st.success("API keys saved to .env file!")

st.set_page_config(page_title="AI Chat Assistant Setup", layout="wide")

st.title("AI Chat Assistant Configuration")

st.header("Enter Your API Keys")

with st.expander("Configure API Keys"):
    qdrant_api_key = st.text_input("Qdrant API Key", type="password")
    email_api_key = st.text_input("Email API Key", type="password")
    scrapeless_api_key = st.text_input("Scrapeless API Key", type="password")

    if st.button("Save API Keys"):
        save_credentials(qdrant_api_key, email_api_key, scrapeless_api_key)