from typing import TypedDict, Any


class TravelState(TypedDict, total=False):
    origin: str
    destination: str
    location: tuple
    preferences: str
    duration: int
    departure_date: str
    return_date: str
    flight_budget: float

    weather: dict[str, Any]
    best_months: list
    best_month: int
    weather_fallback_used: bool
    weather_error: str

    flights: list
    selected_flight: dict

    hotels: list
    selected_hotel: dict

    # Itinerary
    itinerary: str | None
    itinerary_error: str

    error: str
    debug_logs: list[str]