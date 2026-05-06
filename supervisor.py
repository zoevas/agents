from agents.weather import WeatherAgent
from agents.hotel import HotelAgent
from agents.itinerary import ItineraryAgent
from agents.flight import FlightAgent


class SupervisorAgent:
    def __init__(self):
        self.weather = WeatherAgent()
        self.hotel = HotelAgent()
        self.flight = FlightAgent()
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

        flight_out = self.flight.run({
            "origin": user_input["origin"],
            "destination": user_input["destination"],
            "departure_date": user_input["departure_date"],
            "return_date": user_input.get("return_date"),
            "adults": user_input.get("adults", 1),
            "budget": user_input.get("flight_budget"),
        })
        context.update(flight_out)

        hotel_out = self.hotel.run({
            "preferences": user_input["preferences"]
        })
        context.update(hotel_out)

        selected_hotel = context["hotels"][0]

        itinerary_out = self.itinerary.run({
            "destination": user_input["destination"],
            "best_month": best_month,
            "hotel": selected_hotel,
            "duration": user_input["duration"],
            "flight": context["selected_flight"],
        })

        context.update(itinerary_out)
        return context