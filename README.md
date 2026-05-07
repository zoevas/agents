# 🧠 Travel Planner Agents
A modular multi-agent travel planner that combines weather intelligence, hotel search, and LLM-powered itinerary generation.
It was built with:

- LangGraph for workflow orchestration
- MCP (Model Context Protocol) for external services
- Llama.cpp for local itinerary generation
- SentenceTransformers for semantic hotel ranking
- Streamlit for the UI


## A modular multi-agent travel planner

###  1. Install deps
```
pip install -r requirements.txt
```
### 2. Start weather and flight MCP server
From mcp_custom folder, run the following:
```
uvicorn weather_server:app --host 127.0.0.1 --port 8000
uvicorn flight_server:app --host 127.0.0.1 --port 8001
```
### 3. Run app
```
streamlit run app_langgraph.py
```
---

##  Env Setup
```
export OPENWEATHER_API_KEY=your_key
```
---

## How It Works
```
Weather Node
    ↓
Flight Node
    ↓
Hotel Node
    ↓
Itinerary Node
    ↓
Final Travel Plan
```

## Project structure
```
project/
│
├── agents/
│   ├── weather.py
│   ├── flight.py
│   ├── hotel.py
│   └── itinerary.py
	└── base.py
│
├── langgraph_flow/
│   ├── graph.py
│   ├── nodes.py
│   └── state.py
│
├── mcp_custom/
│   ├── flight_client.py
│   ├── weather_client.py
│   ├── flight_server.py
│   └── weather_server.py
│
├── tools/
│   └── hotel_search.py
│
├── models/
│
├── app.py   implementation without langgraph
├── app_langgraph.py
├── requirements.txt
└── README.md
```
---

## MCP Integration (Weather Service, Flight Service)

This project uses MCP (Model Context Protocol) to handle weather data and flight data as separate services.

Flow:
WeatherAgent --> ’MCPWeatherClient’ -->  http://localhost:8000/sse --> MCP Server (weather_server.py) --> OpenWeather API
WeatherAgent --> ’MCPFlightClient’ -->  http://localhost:8001/sse --> MCP Server (flight_server.py) --> Get flight data


### What it does:
- Runs a local weather server
- Exposes get_weather(lat, lon)
- Returns monthly travel scores
- Keeps API logic separate from agents

Similar flow is followed for flight server

### Why It Matters
- Cleaner architecture (agents stay simple)
- Easy to add more services later (flights, maps, etc.)
- Reusable tool layer

---


## Agents

- WeatherAgent - ranks best travel months
- HotelAgent - finds hotels
- FlightAgent - finds flights
- ItineraryAgent - generates itinerary
- SupervisorAgent - orchestrates everything
---
## Weather Scoring
```
score = avg_temp - (rain * 0.5)
Top 3 months are selected automatically.
```
---

## Example Input

```python
{
  "origin": "Athens",
  "destination": "Rome",
  "duration": 5,
  "preferences": "mid budget hotel, city center",
  "departure_date": "2026-06-10"
}
```

## Example Output

```python
{
  "best_month": "May",
  "selected_hotel": {
      "name": "City Center Hotel"
  },
  "selected_flight": {
      "airline": "Aegean Airlines"
  },
  "itinerary": "Day 1..."
}
```
## Error Handling

The workflow supports:

- Weather service fallback
- Empty flight handling
- Missing hotel protection
- Itinerary generation failure logging

Debug logs are stored in graph state:  ```state["debug_logs"]```



---

## Notes

- Requires local LLM model:
  models/llama-2-7b-chat.Q4_K_M.gguf
- Run weather server and flight server before app_langgraph (mcp_custom/server.py  mcp_custom/flight_server.py)
- Supervisor agent auto-selects: best month, first hotel, and first flight

## Future
- Smarter hotel ranking 🏨
- Better UI 🎨
- User selection flow
