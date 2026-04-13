from agents.weather import WeatherAgent
from agents.hotel import HotelAgent
from agents.itinerary import ItineraryAgent

class SupervisorAgent:
    def __init__(self):
        self.weather = WeatherAgent()
        self.hotel = HotelAgent()
        self.itinerary = ItineraryAgent(
            model_path="models/llama-2-7b-chat.Q4_K_M.gguf"
        )

    def execute(self, user_input):
        context = {}

        weather_out = self.weather.run({
            "location": user_input["location"]
        })
        context.update(weather_out)

        best_month = context["best_months"][0]["month"]

        hotel_out = self.hotel.run({
            "preferences": user_input["preferences"]
        })
        context.update(hotel_out)

        selected_hotel = context["hotels"][0]

        itinerary_out = self.itinerary.run({
            "destination": user_input["destination"],
            "best_month": best_month,
            "hotel": selected_hotel,
            "duration": user_input["duration"]
        })

        context.update(itinerary_out)

        return context