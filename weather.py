from typing import Any, Optional, Union, Dict
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("weather")

# Constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"

async def make_nws_request(url: str) -> Optional[dict[str, Optional[str]]]:

    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"Error": str(e)}
        
def format_alert(feature: dict) -> str:
    """
        Format an alert into a readable string
    """

    props = feature["properties"]
    return f"""
        Event: {props.get("Event", "Unknown")}
        Area: {props.get("areaDesc", "Unknown")}
        Severity: {props.get("severity", "Unknown")}
        Description: {props.get("description", "No description available")}
        Instruction: {props.get("instruction", "No specific instructions provided")}
    """

@mcp.tool()
async def get_alerts(state: str) -> Union[Dict, str]:
    """
        Get weather alerts for a US state.

        Args:
            state: Two letter US state code (CA, NY)
    """

    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url=url)

    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found!"
    
    if not data["features"]:
        return "No active alerts for this state"
    
    alerts = [format_alert(feature) for feature in data["features"]]