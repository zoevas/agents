import asyncio
import json
import threading
from mcp import ClientSession
from mcp.client.sse import sse_client


class MCPFlightClient:
    def __init__(self, url="http://localhost:8001/sse"):
        self.url = url

    async def _call_tool(
        self,
        origin,
        destination,
        departure_date,
        return_date=None,
        passengers=1,   # 👈 keep passengers
        budget=None,
    ):
        async with sse_client(self.url) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()

                result = await session.call_tool(
                    "search_flights",
                    {
                        "origin": origin,
                        "destination": destination,
                        "departure_date": departure_date,
                        "return_date": return_date,
                        "adults": passengers,  # 👈 map passengers → adults
                        "budget": budget,
                    },
                )

                # ✅ Prefer structured content
                if getattr(result, "structuredContent", None):
                    return result.structuredContent

                # ✅ Fallback parsing
                if result.content and len(result.content) > 0:
                    text = getattr(result.content[0], "text", None)

                    if not text:
                        return {"error": "Empty text response"}

                    try:
                        return json.loads(text)
                    except json.JSONDecodeError:
                        return {"text": text}

                return {"error": "Empty response"}

    def search_flights(
        self,
        origin,
        destination,
        departure_date,
        return_date=None,
        passengers=1,   # 👈 keep passengers
        budget=None,
    ):
        result = {}

        def runner():
            nonlocal result
            result = asyncio.run(
                self._call_tool(
                    origin,
                    destination,
                    departure_date,
                    return_date,
                    passengers,
                    budget,
                )
            )

        thread = threading.Thread(target=runner)
        thread.start()
        thread.join()

        return result