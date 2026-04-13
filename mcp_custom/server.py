from mcp.server.fastmcp import FastMCP
import os
import requests
import statistics
from datetime import datetime

# Initialize MCP server
mcp = FastMCP("weather-server")

@mcp.tool()
def get_weather(lat: float, lon: float) -> dict:
    """
    Get weather forecast and compute monthly travel scores.
    Score = avg_temp - (total_rain * 0.5). Higher is better for travel.
    """
    api_key = os.getenv("OPENWEATHER_API_KEY", "8151d4e8555fe477fc50fc549c8b694f")
    if not api_key:
        return {"error": "Set OPENWEATHER_API_KEY env var"}

    url = "https://api.openweathermap.org/data/2.5/forecast"
    try:
        resp = requests.get(url, params={
            "lat": lat, "lon": lon, "appid": api_key, "units": "metric"
        }, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        return {"error": f"API failed: {str(e)}"}

    monthly_data = {month: {"temps": [], "rain": []} for month in range(1, 13)}
    for item in data.get("list", []):
        dt = datetime.fromtimestamp(item["dt"])
        month = dt.month
        temp = item["main"]["temp"]
        rain = item.get("rain", {}).get("3h", 0)
        monthly_data[month]["temps"].append(temp)
        monthly_data[month]["rain"].append(rain)

    monthly_scores = []
    for month in range(1, 13):
        temps = monthly_data[month]["temps"]
        rain = monthly_data[month]["rain"]
        avg_temp = statistics.mean(temps) if temps else 0
        total_rain = sum(rain)
        score = avg_temp - (total_rain * 0.5)
        monthly_scores.append({"month": month, "score": float(score)})

    return {"monthly_scores": monthly_scores, "location": f"{lat},{lon}"}

if __name__ == "__main__":
    mcp.run(transport="sse") # ✅ Change to this