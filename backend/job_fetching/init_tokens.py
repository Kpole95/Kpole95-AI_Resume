
import json
import os
import requests
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv

# Setup paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
TOKEN_FILE = BASE_DIR / "config" / "tokens.json"

# Function to get credentials securely
def get_credentials():
    """
    Gets credentials either from Streamlit's secrets manager (for deployment)
    or from local files (for development).
    """
    # to Check if the app is running on Streamlit Cloud
    if hasattr(st, 'secrets'):
        return {
            "client_id": st.secrets.get("CLIENT_ID"),
            "client_secret": st.secrets.get("CLIENT_SECRET"),
            "access_token": st.secrets.get("ACCESS_TOKEN"),
            "refresh_token": st.secrets.get("REFRESH_TOKEN")
        }
    else:
        # local
        load_dotenv(BASE_DIR / ".env")
        try:
            with open(TOKEN_FILE, 'r') as f:
                tokens = json.load(f)
            return {
                "client_id": os.getenv("CLIENT_ID"),
                "client_secret": os.getenv("CLIENT_SECRET"),
                "access_token": tokens.get("access_token"),
                "refresh_token": tokens.get("refresh_token")
            }
        except FileNotFoundError:
            return {"client_id": os.getenv("CLIENT_ID"), "client_secret": os.getenv("CLIENT_SECRET")}

def validate_token(access_token):
    """Validates if the current access token is still active."""
    url = "https://api.hh.ru/vacancies?per_page=1"
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def refresh_token():
    """Refreshes the hh.ru API token using available credentials."""
    creds = get_credentials()
    if not creds.get("refresh_token"):
        raise ValueError("No refresh token available to refresh.")

    print("Refreshing hh.ru token...")
    url = "https://api.hh.ru/token"
    data = {
        "grant_type": "refresh_token",
        "refresh_token": creds["refresh_token"],
        "client_id": creds["client_id"],
        "client_secret": creds["client_secret"]
    }
    response = requests.post(url, data=data, timeout=10)

    if response.status_code == 200:
        new_tokens = response.json()
        new_access_token = new_tokens["access_token"]
        
        # local
        if not hasattr(st, 'secrets'):
            with open(TOKEN_FILE, 'w') as f:
                json.dump(new_tokens, f, indent=4)
            print("Updated local tokens.json with new access token.")
        
        return new_access_token
    else:
        raise Exception(f"Token refresh failed: {response.text}")