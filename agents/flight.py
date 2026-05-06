from agents.base import Agent
from mcp_custom.flight_client import MCPFlightClient


class FlightAgent(Agent):
    def __init__(self):
        super().__init__("FlightAgent")
        self.client = MCPFlightClient("http://localhost:8001/sse")

    def run(self, input_data):
        result = self.client.search_flights(
            origin=input_data["origin"],
            destination=input_data["destination"],
            departure_date=input_data["departure_date"],
            passengers=input_data.get("passengers", 1),
        )

        flights = result.get("flights", [])
        if not flights:
            raise ValueError("No flights found")

        return {"flights": flights,
                "selected_flight": flights[0],
}