from agents.base import Agent
from tools.hotel_search import search_hotels

class HotelAgent(Agent):
    def __init__(self):
        super().__init__("HotelAgent")

    def run(self, input_data):
        hotels = search_hotels(input_data["preferences"])

        if not hotels:
            raise ValueError("No hotels found")

        return {"hotels": hotels}