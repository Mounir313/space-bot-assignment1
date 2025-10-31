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

def list_rooms(access_token: str) -> list[dict]:
    url = f"{WEBEX_BASE}/rooms"
    r = requests.get(url, headers=webex_headers(access_token))
    ensure_ok(r)
    rooms = r.json().get("items", [])
    print("List of rooms:")
    for room in rooms:
        print(f"Type: '{room.get('type')}' Name: {room.get('title')}")
    return rooms

def pick_room(rooms: list[dict]) -> dict:
    query = input("Which room should be monitored for /seconds messages? ").strip()
    matches = [r for r in rooms if query.lower() in (r.get("title") or "").lower()]
    if not matches:
        raise ValueError(f"No rooms found with the word {query}")
    print(f"Found rooms with the word {query}")
    chosen = matches[0]
    print(f"Found room : {chosen.get('title')}")
    return chosen

def get_latest_message(access_token: str, room_id: str) -> Optional[str]:
    url = f"{WEBEX_BASE}/messages"
    params = {"roomId": room_id, "max": 1}
    r = requests.get(url, headers=webex_headers(access_token), params=params)
    ensure_ok(r)
    items = r.json().get("items", [])
    if not items:
        return None
    return items[0].get("text")

def parse_seconds(msg: str) -> Optional[int]:
    if not msg:
        return None
    msg = msg.strip()
    if msg.startswith("/") and msg[1:].isdigit():
        return int(msg[1:])
    return None

def get_iss_location(timeout: int = 5) -> dict:
    r = requests.get(ISS_URL, timeout=timeout)
    ensure_ok(r)
    data = r.json()
    lat = data["iss_position"]["latitude"]
    lon = data["iss_position"]["longitude"]
    ts = data["timestamp"]
    human_time = datetime.datetime.fromtimestamp(ts)
    return {"lat": float(lat), "lon": float(lon), "ts": ts, "human": human_time}





if __name__ == "__main__":
    token = get_token()
    print("Token loaded.")

