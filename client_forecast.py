import asyncio
import nest_asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client

nest_asyncio.apply()

async def get_forecast_for_city(city_name: str, lat: float, lon: float):
    """Get weather forecast for a specific city"""
    try:
        print(f"🌤️  Connecting to get forecast for {city_name}...")
        async with sse_client("http://localhost:8000/sse") as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                print(f"✅ Connected to server for {city_name}")
                
                # Get forecast
                result = await session.call_tool("get_forecast", arguments={
                    "latitude": lat, 
                    "longitude": lon
                })
                
                print(f"\n📊 FORECAST FOR {city_name.upper()}:")
                print("=" * 50)
                print(result.content[0].text)
                print("=" * 50)
                
    except Exception as e:
        print(f"Error getting forecast for {city_name}: {e}")

async def main():
    # Multiple cities to demonstrate concurrent connections
    cities = [
        ("San Francisco", 37.7749, -122.4194),
        ("Los Angeles", 34.0522, -118.2437),
        ("New York", 40.7128, -74.0060),
        ("Miami", 25.7617, -80.1918)
    ]
    
    print("🌍 MULTI-CLIENT WEATHER FORECAST DEMO")
    print("=" * 40)
    
    # Run all forecasts concurrently
    tasks = [get_forecast_for_city(city, lat, lon) for city, lat, lon in cities]
    await asyncio.gather(*tasks)
    
    print("\n🎉 All forecasts completed!")

if __name__ == "__main__":
    asyncio.run(main())
