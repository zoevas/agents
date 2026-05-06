from langgraph.graph import StateGraph, END
from langgraph_flow.state import TravelState
from langgraph_flow.nodes import (
    weather_node,
    flight_node,
    hotel_node,
    itinerary_node,
)


def build_graph():
    graph = StateGraph(TravelState)

    graph.add_node("weather", weather_node)
    graph.add_node("flight", flight_node)
    graph.add_node("hotel", hotel_node)
    graph.add_node("itinerary", itinerary_node)

    graph.set_entry_point("weather")

    graph.add_edge("weather", "flight")
    graph.add_edge("flight", "hotel")
    graph.add_edge("hotel", "itinerary")
    graph.add_edge("itinerary", END)

    return graph.compile()