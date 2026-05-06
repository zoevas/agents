from agents.weather import WeatherAgent
from agents.flight import FlightAgent
from agents.hotel import HotelAgent
from agents.itinerary import ItineraryAgent

def add_log(state, message):
    if "debug_logs" not in state:
        state["debug_logs"] = []

    state["debug_logs"].append(message)

def weather_node(state):
    add_log(state, "Running WeatherAgent")

    try:
        result = WeatherAgent().run({
         "location": state["location"]
        })

        state.update(result)
        state["best_month"] = result["best_months"][0]["month"]
        state["weather_fallback_used"] = False
        add_log(state, "Weather success")

    except Exception as e:
        state["weather_error"] = str(e)
        state["best_months"] = []
        state["best_month"] = None
        state["weather_fallback_used"] = True

        add_log(state, f"Weather failed: {str(e)}")

    return state


def flight_node(state):
    result = FlightAgent().run({
        "origin": state["origin"],
        "destination": state["destination"],
        "departure_date": state["departure_date"],
        "return_date": state.get("return_date"),
        "budget": state.get("flight_budget"),
        "passengers": 1,
    })

    state.update(result)
    return state


def hotel_node(state):
    result = HotelAgent().run({
        "preferences": state["preferences"]
    })

    state.update(result)
    state["selected_hotel"] = result["hotels"][0]
    return state


def add_log(state, message):
    if "debug_logs" not in state:
        state["debug_logs"] = []
    state["debug_logs"].append(message)


def itinerary_node(state):
    add_log(state, "Running ItineraryAgent")

    if not state.get("selected_hotel"):
        state["itinerary_error"] = "Cannot generate itinerary without selected hotel"
        state["itinerary"] = None

        add_log(state, "Itinerary failed: no selected hotel")

        return state

    try:
        result = ItineraryAgent(
            model_path="models/llama-2-7b-chat.Q4_K_M.gguf"
        ).run({
            "destination": state["destination"],
            "best_month": state.get("best_month"),
            "hotel": state["selected_hotel"],
            "flight": state.get("selected_flight"),
            "duration": state["duration"],
        })

        state.update(result)

        add_log(state, "Itinerary generated successfully")

    except Exception as e:
        state["itinerary_error"] = str(e)
        state["itinerary"] = None

        add_log(state, f"Itinerary failed: {str(e)}")

    return state