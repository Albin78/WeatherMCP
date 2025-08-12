import asyncio
import nest_asyncio
from mcp import ClientSession
from mcp.client.stdio import stdio_client

nest_asyncio.apply()  # Needed to run interactive python

"""
Make sure
1. The server is running with stdio transport
2. This client connects to the server's stdio interface
3. Use this for direct process-to-process communication

"""

async def main():
    # Connect to server using stdio transport
    async with stdio_client() as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            # Initialize the connection
            await session.initialize()
            print("Connected to server via stdio")

            # List available tools
            tools_result = await session.list_tools()
            print("Available tools:")
            for tool in tools_result.tools:
                print(f"    - {tool.name}: {tool.description}\n")
            
            # Call the weather forecast tool
            result = await session.call_tool("get_forecast", arguments={
                "latitude": 37.7749, 
                "longitude": -122.4194
            })
            print(f"The weather forecast for San Francisco is = {result.content[0].text}")

if __name__ == "__main__":
    asyncio.run(main())
