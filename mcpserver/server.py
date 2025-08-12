import time
from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# creating an MCP server
mcp = FastMCP(
    name="weather",
    host="0.0.0.0", # only used for SSE transport (localhost)
    port=8000,  # only used for SSE transport
)

# constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"

async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling"""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url=url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

def format_alert(feature: dict) -> str:
    """Format an alert feature into a readable string"""
    props = feature["properties"]
    return f"""
    Event: {props.get('event','Unknown')}
    Area: {props.get('areaDesc', 'Unknown')}
    Severity: {props.get('severity', 'Unknown')}
    Description: {props.get('description', 'No description available')}
    Instruction: {props.get('instruction', 'No specific instruction provided')}
    """

@mcp.tool()
async def get_forecast(longitude: float, latitude: float) -> str:
    """ Get weather forecast for given longitude and latitude""" 
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)

    if not points_data:
        return "Unable to forecast data for this location"

    # Getting the forecast url from points response
    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_nws_request(forecast_url)

    if not forecast_data:
        return "Unable to fetch forecast details"

    periods = forecast_data["properties"]["periods"]
    forecasts = []
    for period in periods[:5]: # only next 5 periods
        forecast = f"""
        {period['name']}:
        Temperature: {period['temperature']}°F
        Wind: {period.get('windSpeed', 'N/A')} {period.get('windDirection', 'N/A')}
        Forecast: {period['detailedForecast']}
        """
        forecasts.append(forecast)
    
    return "\n--\n".join(forecasts)

@mcp.tool()
async def get_result(state: str) -> str:
    """Get weather alerts for a US state"""
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)
    
    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found"
    
    if not data["features"]:
        return "No active alerts for this state"
    
    alerts = []
    for feature in data["features"]:
        props = feature["properties"]
        alert = f"""
        Event: {props.get('event', 'Unknown')}
        Area: {props.get('areaDesc', 'Unknown')}
        Severity: {props.get('severity', 'Unknown')}
        Description: {props.get('description', 'No description available')}
        """
        alerts.append(alert)
    
    return "\n---\n".join(alerts)

# Run the server
if __name__ == "__main__":
    transport = "sse"
    if transport == "stdio":
        print("Running server with stdio transport")
        mcp.run(transport="stdio")
    elif transport == "sse":
        print("Running server with SSE transport")
        mcp.run(transport="sse")
    else:
        raise ValueError(f"Unknown transport: {transport}")
