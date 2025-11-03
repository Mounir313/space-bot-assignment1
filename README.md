# 🚀 Space Bot API Investigation Sheet

**Total Marks: 30**  
**Part 1: Collect Required API Documentation**

This investigation sheet helps you gather key technical information from the three APIs required for the Space Bot project: **Webex Messaging API**, **ISS Current Location API**, and a **Geocoding API** (LocationIQ or Mapbox or other), plus the Python time module.

---

## ✅ Section 1: Webex Messaging API (7 marks)

| Criteria | Details |
|---------|---------|
| API Base URL | `https://webexapis.com/v1` |
| Authentication Method | `HTTP Authorization header: Bearer <access_token>` |
| Endpoint to list rooms | `GET https://webexapis.com/v1/rooms` |
| Endpoint to get messages | `https://webexapis.com/v1/messages?roomId="Y2lzY29zcGFyazovL3VybjpURUFNOnVzLXdlc3QtMl9yL1JPT00vOGY5Mjc2NDAtYjVkNC0xMWYwLTkyODMtOGRjMTZjNmVlMzVk" &max=1` |
| Endpoint to send message | `POST https://webexapis.com/v1/messages` |
Body (JSON): { "roomId": "Y2lzY29zcGFyazovL3VybjpURUFNOnVzLXdlc3QtMl9yL1JPT00vOGY5Mjc2NDAtYjVkNC0xMWYwLTkyODMtOGRjMTZjNmVlMzVk", "text": "Hello room!" }` |
| Required headers | `Authorization: Bearer <token>` and for POST: `Content-Type: application/json` |
| Sample full GET or POST request | `Sample full GET (rooms)
curl -H "Authorization: Bearer <TOKEN>" "https://webexapis.com/v1/rooms"

Sample POST (send message)
curl -X POST -H "Authorization: Bearer <TOKEN>" -H "Content-Type: application/json" \
  -d '{"roomId":"Y2lzY29zcGFyazovL3VybjpURUFNOnVzLXdlc3QtMl9yL1JPT00vOGY5Mjc2NDAtYjVkNC0xMWYwLTkyODMtOGRjMTZjNmVlMzVk","text":"Hello room!"}' \
  "https://webexapis.com/v1/messages"` |

---

## 🛰️ Section 2: ISS Current Location API (3 marks)

| Criteria | Details |
|---------|---------|
| API Base URL | `http://api.open-notify.org` |
| Endpoint for current ISS location | `GET http://api.open-notify.org/iss-now.json` |
| Sample response format (example JSON) |  
```
{
    "message": "success",
    "timestamp": 1762051489,
    "iss_position": {
        "longitude": "-31.2013",
        "latitude": "49.4976"
    }
}
```
|

---

## 🗺️ Section 3: Geocoding API (LocationIQ or Mapbox or other) (6 marks)

| Criteria | Details |
|---------|---------|
| Provider used (circle one) | **LocationIQ** |
| API Base URL | `https://us1.locationiq.com/v1` |
| Endpoint for reverse geocoding | `GET /reverse?key=pk.b1855e16f4d5edb8749a7d83e2d51847&lat=49.4976&lon=-31.2013&format=json` |
| Authentication method | `API key via query parameter `key=pk.b1855e16f4d5edb8749a7d83e2d51847` |
| Required query parameters | `key`, `lat`, `lon`, `format=json` |
| Sample request with latitude/longitude | `https://us1.locationiq.com/v1/reverse?key=pk.b1855e16f4d5edb8749a7d83e2d51847&lat=49.4976&lon=-31.2013&format=json` |
| Sample JSON response (formatted example) |  
```json
{
  "lat": "49.4976",
  "lon": "-31.2013",
  "address": {
    "road": "Butterfield Trl",
    "city": "Imperial",
    "state": "CA",
    "country": "United States of America",
    "country_code": "us"
  },
  "display_name": "Butterfield Trl, Imperial, CA, United States of America"
}
Sometimes it gives me “Unable to geocode” is not that my code is broken — it’s because the coordinates I tested are in the middle of the ocean, where LocationIQ has no street‑level address to return. The API is working correctly, but it can only return an address if the point is on land where data exists. but it should look like the example above.

```
|

---

## ⏰ Section 4: Epoch to Human Time Conversion (Python time module) (2 marks)

| Criteria | Details |
|---------|---------|
| Library used | `datetime` |
| Function used to convert epoch | `datetime.datetime.fromtimestamp(1762051489)` |
| Sample code to convert timestamp |  
```  Epoch: 1762051489
Human-readable: Sat Nov  2 04:04:49 2025
ISS Position → Latitude: 49.4976, Longitude: -31.2013

```
|
| Output (human-readable time) | `Sat Nov 2 04:04:49 2025` |

---

## 🧩 Section 5: Web Architecture & MVC Design Pattern (12 marks)

### 🌐 Web Architecture – Client-Server Model

- **Client**:  Python bot and Webex client (user side).
- **Server**:  Webex REST API, ISS API, LocationIQ API. 
- Client sends HTTP requests (GET/POST) with headers; servers return JSON. Bot parses JSON, transforms data, and posts results back to Webex.

### 🔁 RESTful API Usage

- **Resources:** Rooms (`/rooms`), messages (`/messages`), ISS location (`/iss-now.json`), reverse geocode (`/reverse`).  
- **Methods:** GET to retrieve data, POST to create messages.
- **Representations:** JSON payloads; bot handles status codes (200 OK) and errors (404 not found).

### 🧠 MVC Pattern in Space Bot

| Component   | Description |
|------------|-------------|
| **Model**  | Holds data structures and state |
| **View**   | Presentation layer (what the user sees) |
| **Controller** | Logic that orchestrates everything |


#### Example:
- Model: data = {'lat': 49.4976, 'lon': -31.2013, 'timestamp': 1762051489}
- View: Webex client shows: “On Mon Nov 03 01:40:53 2025, the ISS was flying over Pedregal, Chiriquí, Panama (8.2570°, -82.3292°). `markdown_message = f"On {time_str}, the ISS was flying over {place} ({lat}°, {lon}°)"`
- Controller: `main()` reads messages, waits seconds, calls `get_iss_location()`, `reverse_geocode()`, and `post_message()`.

---

### 📝 Notes

- Use official documentation for accuracy (e.g. developer.webex.com, locationiq.com or Mapbox, open-notify.org or other ISS API).
- Be prepared to explain your findings to your instructor or demo how you retrieved them using tools like Postman, Curl, or Python scripts.

---

### ✅ Total: /30

