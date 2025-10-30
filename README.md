# 🚀 Space Bot API Investigation Sheet

**Total Marks: 30**  
**Part 1: Collect Required API Documentation**

This investigation sheet gathers key technical information for the Space Bot project: **Webex Messaging API**, **ISS Current Location API**, a **Geocoding API (LocationIQ)**, plus the Python time module.

---

## ✅ Section 1: Webex Messaging API (7 marks)

| Criteria | Details |
|---------|---------|
| API Base URL | `https://webexapis.com/v1` |
| Authentication Method | `HTTP Authorization header: Bearer <access_token>` |
| Endpoint to list rooms | `GET /rooms` |
| Endpoint to get messages | `GET /messages?roomId=<room_id>&max=1` |
| Endpoint to send message | `POST /messages` |
| Required headers | `Authorization: Bearer <token>` and for POST: `Content-Type: application/json` |
| Sample full GET or POST request | **GET:** `curl -H "Authorization: Bearer $TOKEN" "https://webexapis.com/v1/rooms"`<br>**POST:** `curl -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d '{"roomId":"<id>","markdown":"Hello"}' https://webexapis.com/v1/messages` |

---

## 🛰️ Section 2: ISS Current Location API (3 marks)

| Criteria | Details |
|---------|---------|
| API Base URL | `http://api.open-notify.org` |
| Endpoint for current ISS location | `GET /iss-now.json` |
| Sample response format (example JSON) |  
```json
{
  "message": "success",
  "timestamp": 1730149890,
  "iss_position": { "latitude": "7.0680", "longitude": "-61.2094" }
}
``` |

---

## 🗺️ Section 3: Geocoding API (LocationIQ) (6 marks)

| Criteria | Details |
|---------|---------|
| Provider used | LocationIQ |
| API Base URL | `https://us1.locationiq.com/v1` |
| Endpoint for reverse geocoding | `GET /reverse?key=<API_KEY>&lat=<LAT>&lon=<LON>&format=json` |
| Authentication method | API key via query parameter `key=<API_KEY>` |
| Required query parameters | `key`, `lat`, `lon`, `format=json` |
| Sample request with latitude/longitude | `https://us1.locationiq.com/v1/reverse?key=YOUR_KEY&lat=7.0680&lon=-61.2094&format=json` |
| Sample JSON response (formatted example) |  
```json
{
  "lat": "7.0680",
  "lon": "-61.2094",
  "address": {
    "road": "Butterfield Trl",
    "city": "Imperial",
    "state": "CA",
    "country": "United States of America",
    "country_code": "us"
  },
  "display_name": "Butterfield Trl, Imperial, CA, United States of America"
}
``` |

---

## ⏰ Section 4: Epoch to Human Time Conversion (Python time module) (2 marks)

| Criteria | Details |
|---------|---------|
| Library used | `datetime` |
| Function used to convert epoch | `datetime.datetime.fromtimestamp(<epoch>)` |
| Sample code to convert timestamp |  
```python
import datetime
human_time = datetime.datetime.fromtimestamp(1730149890)
print(human_time.ctime())  # e.g., 'Wed Oct 29 22:51:30 2025'
``` |
| Output (human-readable time) | `Wed Oct 29 22:51:30 2025` |

---

## 🧩 Section 5: Web Architecture & MVC Design Pattern (12 marks)

### 🌐 Web Architecture – Client-Server Model

- **Client:** Python bot and Webex client (user side).  
- **Server:** Webex REST API, ISS API, LocationIQ API.  
- **Communication:** Client sends HTTP requests (GET/POST) with headers; servers return JSON. Bot parses JSON, transforms data, and posts results back to Webex.

### 🔁 RESTful API Usage

- **Resources:** Rooms (`/rooms`), messages (`/messages`), ISS location (`/iss-now.json`), reverse geocode (`/reverse`).  
- **Methods:** GET to retrieve data, POST to create messages.  
- **Representations:** JSON payloads; bot handles status codes (200 OK) and errors (4xx/5xx).

### 🧠 MVC Pattern in Space Bot

| Component   | Description |
|------------|-------------|
| **Model**  | Data structures holding token, room IDs, ISS coordinates, geocode results, and timestamps. |
| **View**   | Webex message content (markdown text) rendered in the room for users. |
| **Controller** | Python functions orchestrating API calls, parsing, timing (/seconds), and posting formatted output. |

**Example:**  
- Model: `iss_data = {"lat": ..., "lon": ..., "timestamp": ...}`  
- View: `markdown_message = f"On {time_str}, the ISS was flying over {place} ({lat}°, {lon}°)"`  
- Controller: `main()` reads messages, waits seconds, calls `get_iss_location()`, `reverse_geocode()`, and `post_message()`.

---

### ✅ Total: /30



