from mcp.server.fastmcp import FastMCP

mcp = FastMCP("flight-server")


@mcp.tool()
def search_flights(
    origin: str,
    destination: str,
    departure_date: str,
    return_date: str | None = None,
    adults: int = 1,
    budget: float | None = None,
) -> dict:
    """
    Search for flights between two airports/cities.
    Returns a normalized list of flight options.
    """

    flights = [
        {
            "airline": "Aegean",
            "origin": origin,
            "destination": destination,
            "departure_date": departure_date,
            "return_date": return_date,
            "departure_time": "09:30",
            "arrival_time": "11:45",
            "price": 180.0,
            "currency": "EUR",
        },
        {
            "airline": "Lufthansa",
            "origin": origin,
            "destination": destination,
            "departure_date": departure_date,
            "return_date": return_date,
            "departure_time": "14:10",
            "arrival_time": "16:35",
            "price": 220.0,
            "currency": "EUR",
        },
    ]

    if budget is not None:
        flights = [f for f in flights if f["price"] <= budget]

    return {
        "flights": flights,
        "count": len(flights),
    }


app = mcp.sse_app()