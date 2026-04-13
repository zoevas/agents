from agents.base import Agent
from mcp_custom.client import MCPWeatherClient

class WeatherAgent(Agent):
    def __init__(self):
        super().__init__("WeatherAgent")
        self.client = MCPWeatherClient("http://localhost:8000/sse")

    def run(self, input_data):
        lat, lon = input_data["location"]
        weather = self.client.get_weather(lat, lon)
        print("DEBUG FULL WEATHER:", weather)

        # ✅ SAFE dictionary access - NO KeyError
        if "error" in weather or "monthly_scores" not in weather:
            print("❌ Weather error or no scores, using fallback")
            monthly_scores = [{"month": i, "score": 0.0} for i in range(1, 13)]
        else:
            monthly_scores = weather["monthly_scores"]

        # ✅ Top 3 best months
        best_months = sorted(monthly_scores, key=lambda x: x["score"], reverse=True)[:3]

        print(f"✅ BEST MONTHS: {best_months}")

        return {
            "weather": weather,
            "monthly_scores": monthly_scores,
            "best_months": best_months  # Supervisor expects this!
        }