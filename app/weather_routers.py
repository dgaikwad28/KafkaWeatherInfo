import os
from typing import Optional

import requests

from app import settings


# Function to get current weather using the OpenWeatherMap API
def get_current_weather(lat: float, long: float) -> Optional[dict]:
    complete_url = f"{settings.OWM_BASE_URL}?lat={lat}&lon={long}&appid={settings.OWM_API_KEY}"

    response = requests.get(complete_url)
    if response.status_code == 200:
        weather_data = response.json()
        return {
            "weather": weather_data["weather"],
            "city": weather_data["name"],
            "country": weather_data["sys"]["country"],
        }
    else:
        return None
