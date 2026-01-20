import httpx
from typing import Dict, Any


class ExternalWeatherService:
    def __init__(self, base_url: str = "https://api.open-meteo.com/v1"):
        self.base_url = base_url

    async def get_current_weather(
        self, latitude: float, longitude: float
    ) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/forecast",
                params={
                    "latitude": latitude,
                    "longitude": longitude,
                    "current_weather": True,
                },
            )
            response.raise_for_status()
            return response.json()
