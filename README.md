# 🧠 Travel Planner Agents
A modular multi-agent travel planner that combines weather intelligence, hotel search, and LLM-powered itinerary generation.

## A modular multi-agent travel planner that combines weather intelligence, hotel search, and LLM-powered itinerary generation.
```bash
# 1. Install deps
pip install -r requirements.txt

# 2. Start weather MCP server
python server.py

# 3. Run app
streamlit run app.py
```

#How It Works
User Input
   ↓
SupervisorAgent
   ├── WeatherAgent → best months
   ├── HotelAgent → hotels
   └── ItineraryAgent → trip plan
   ↓
Final Travel Plan

---

## MCP Integration (Weather Service)

This project uses MCP (Model Context Protocol) to handle weather data as a separate service.

Flow:
WeatherAgent --> ’MCPWeatherClient’ -->  http://localhost:8000/sse --> MCP Server (server.py) --> OpenWeather API

### What it does:
- Runs a local weather server
- Exposes get_weather(lat, lon)
- Returns monthly travel scores
- Keeps API logic separate from agents

### Why It Matters
- Cleaner architecture (agents stay simple)
- Easy to add more services later (flights, maps, etc.)
- Reusable tool layer

---


## Agents

- WeatherAgent - ranks best travel months
- HotelAgent - finds hotels
- ItineraryAgent - generates itinerary
- SupervisorAgent - orchestrates everything
---

## Example Input

```python
{
  "location": (48.85, 2.35),
  "destination": "Paris",
  "duration": 5,
  "preferences": {"budget": "mid"}
}
```

---
---

## Weather Scoring

score = avg_temp - (rain * 0.5)
Top 3 months are selected automatically.

---

##  Env Setup

export OPENWEATHER_API_KEY=your_key

---

## Notes

- Requires local LLM model:
  models/llama-2-7b-chat.Q4_K_M.gguf
- Run weather server before app (mcp_custom/server.py)
- Supervisor auto-selects: best month, first hotel

## Future
- Flight agent ✈️
- Smarter hotel ranking 🏨
- Better UI 🎨
- User selection flow