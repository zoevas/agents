import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client
from concurrent.futures import ThreadPoolExecutor
import asyncio
import threading
import json

class MCPWeatherClient:
    def __init__(self, url="http://localhost:8000/sse"):
        self.url = url


    async def _call_tool(self, lat, lon):
        async with sse_client(self.url) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()

                result = await session.call_tool(
                    "get_weather",
                    {"lat": lat, "lon": lon}
                )

                # ✅ Extract and parse JSON
                if result.content and len(result.content) > 0:
                    text = result.content[0].text
                    return json.loads(text)

                return {"error": "Empty response"}



    def get_weather(self, lat, lon):
        result = {}

        def runner():
            nonlocal result
            result = asyncio.run(self._call_tool(lat, lon))

        thread = threading.Thread(target=runner)
        thread.start()
        thread.join()

        return result