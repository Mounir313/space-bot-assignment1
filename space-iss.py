import os
import time
import json
import requests
import datetime
from typing import Optional, Dict, Any
from dotenv import load_dotenv

load_dotenv()

WEBEX_BASE = "https://webexapis.com/v1"
ISS_URL = "http://api.open-notify.org/iss-now.json"
LOCATIONIQ_BASE = "https://us1.locationiq.com/v1"

def get_token() -> str:
    choice = input("Do you want to enter the Webex access token now? (Y/N): ").strip().lower()
    if choice == "y":
        raw = input("Enter your Webex token (without 'Bearer '): ").strip()
        return f"Bearer {raw}"
    env_token = os.getenv("WEBEX_TOKEN")
    if env_token and env_token.startswith("Bearer "):
        return env_token
    raise ValueError("No token provided. Set WEBEX_TOKEN in .env as 'Bearer <token>' or enter one.")

def webex_headers(access_token: str) -> Dict[str, str]:
    return {"Authorization": access_token, "Content-Type": "application/json"}

def ensure_ok(r: requests.Response) -> None:
    if r.status_code != 200:
        raise Exception(f"Bad status {r.status_code}: {r.text}")

if __name__ == "__main__":
    token = get_token()
    print("Token loaded.")

