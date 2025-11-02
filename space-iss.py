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

ISS_URL = "http://api.open-notify.org/iss-now.json"

def get_iss_location() -> dict:
    r = requests.get(ISS_URL, timeout=10)
    r.raise_for_status()
    data = r.json()   # store JSON in 'data'

    ts = data["timestamp"]
    lat = float(data["iss_position"]["latitude"])
    lon = float(data["iss_position"]["longitude"])

    return {
        "lat": lat,
        "lon": lon,
        "ts": ts,
        "human": datetime.datetime.fromtimestamp(ts)
    }


def reverse_geocode(lat: float, lon: float) -> Dict[str, Any]:
    key = os.getenv("LOCATIONIQ_KEY")
    if not key:
        raise ValueError("LOCATIONIQ_KEY missing in .env")
    url = f"{LOCATIONIQ_BASE}/reverse"
    params = {"key": key, "lat": lat, "lon": lon, "format": "json"}
    r = requests.get(url, params=params, timeout=8)
    ensure_ok(r)
    data = r.json()
    addr = data.get("address", {})
    return {
        "road": addr.get("road"),
        "city": addr.get("city") or addr.get("town") or addr.get("village"),
        "state": addr.get("state"),
        "country": addr.get("country"),
        "code": addr.get("country_code"),
        "display": data.get("display_name"),
    }


def format_location_message(human: datetime.datetime, lat: float, lon: float, geo: Dict[str, Any]) -> str:
    time_str = human.ctime()
    parts = []
    if geo.get("city"): parts.append(geo["city"])
    if geo.get("state"): parts.append(geo["state"])
    if geo.get("country"): parts.append(geo["country"])
    location_str = ", ".join(parts) if parts else (geo.get("display") or "an unknown location")
    return f"On {time_str}, the ISS was flying over {location_str}. ({lat:.4f}°, {lon:.4f}°)"

def post_message(access_token: str, room_id: str, markdown_text: str) -> None:
    url = f"{WEBEX_BASE}/messages"
    payload = {"roomId": room_id, "markdown": markdown_text, "text": markdown_text}
    r = requests.post(url, headers=webex_headers(access_token), data=json.dumps(payload))
    ensure_ok(r)

def main():
    access_token = get_token()
    rooms = list_rooms(access_token)
    chosen = pick_room(rooms)
    room_id = chosen["id"]

    print("Starting ISS monitor (Ctrl+C to stop)...")
    last_seen = None

    while True:
        try:
            msg = get_latest_message(access_token, room_id)

            if msg and msg != last_seen:
                print(f"Received message: {msg}")
                last_seen = msg

                secs = parse_seconds(msg)
                if secs is not None:
                    wait_for = max(0, min(secs, 300))  
                    print(f"Waiting {wait_for} seconds...")
                    time.sleep(wait_for)

                    iss_data = get_iss_location()
                    lat, lon, ts = iss_data["latitude"], iss_data["longitude"], iss_data["timestamp"]

                    human_time = datetime.datetime.fromtimestamp(ts)

                    geo = reverse_geocode(lat, lon)

                    response = format_location_message(human_time, lat, lon, geo)
                    print(f"Sending to Webex: {response}")
                    post_message(access_token, room_id, response)

            time.sleep(1)

        except KeyboardInterrupt:
            print("Exiting monitor.")
            break
        except Exception as e:
            print(f"Warning: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()


