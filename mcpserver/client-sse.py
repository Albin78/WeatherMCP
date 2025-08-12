import asyncio
import nest_asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client

nest_asyncio.apply()  # Needed to run interactive python

"""
Make sure
1. The server is running before this script
2. The server is configured to use SSE transport
3. The server is listening on port 8000

"""

async def main():
    # Connect to server using SSE
    async with sse_client("http://localhost:8000/sse") as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            # initialize the connection
            await session.initialize()

            # List available tools
            tools_result = await session.list_tools()
            print("Available tools:")
            for tool in tools_result.tools:
                print(f"    - {tool.name}: {tool.description}\n")
            
            # call the weather forecast tool
            result = await session.call_tool("get_forecast", arguments={"latitude": 37.7749, "longitude": -122.4194})
            print(f"The weather forecast for San Francisco is = {result.content[0].text}")

if __name__ == "__main__":
    asyncio.run(main())
