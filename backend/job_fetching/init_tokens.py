import requests
import json
from pathlib import Path
import os

# local development
BASE_DIR = Path(__file__).resolve().parent.parent.parent
TOKEN_FILE = BASE_DIR / "config" / "tokens.json"

def get_credentials():
    """
    Gets credentials securely. For deployment, it reads from environment variables
    (which are set by Hugging Face Secrets). For local development, it falls
    back to the tokens.json file.
    """
    # Docker Space on Hugging Face
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    
    if client_id and client_secret:
        print("INFO: Found CLIENT_ID and CLIENT_SECRET in environment variables (deployment).")
        # In deployment get the initial tokens from secrets as well
        access_token = os.getenv("ACCESS_TOKEN")
        refresh_token = os.getenv("REFRESH_TOKEN")
        return client_id, client_secret, access_token, refresh_token
    else:
        # this is the fallback for local machine
        print("INFO: Could not find environment variables. Using local config/tokens.json.")
        with open(TOKEN_FILE, 'r') as f:
            data = json.load(f)
        return data.get("client_id"), data.get("client_secret"), data.get("access_token"), data.get("refresh_token")

def refresh_token():
    """Refreshes the hh.ru API token using the fetched credentials."""
    client_id, client_secret, _, refresh_token_val = get_credentials()
    if not client_id or not client_secret:
        raise Exception("Client ID or Client Secret not found.")
    if not refresh_token_val:
        # this case is for the very first run if no refresh token exists
        # it will get a token using client_credentials grant type
        data = {'grant_type': 'client_credentials', 'client_id': client_id, 'client_secret': client_secret}
    else:
        data = {'grant_type': 'refresh_token', 'refresh_token': refresh_token_val}
        
    try:
        print("INFO: Requesting new token from hh.ru...")
        response = requests.post('https://api.hh.ru/token', data=data, timeout=10)
        response.raise_for_status()
        tokens = response.json()
        print("INFO: New access token received.")
        return tokens.get("access_token")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error refreshing token: {e}")

def validate_token(token):
    """Validates the current token by making a lightweight API call."""
    try:
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get('https://api.hh.ru/me', headers=headers, timeout=10)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False