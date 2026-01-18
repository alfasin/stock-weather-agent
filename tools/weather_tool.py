"""Weather forecast tool using Open-Meteo API with caching."""

import json
from datetime import date
from pathlib import Path

import requests

from config import CACHE_DIR, DEFAULT_CITY, get_city_coordinates
from mock_data import get_mock_weather

# WMO Weather interpretation codes
# https://open-meteo.com/en/docs
WMO_CODES = {
    0: "clear sky",
    1: "mainly clear",
    2: "partly cloudy",
    3: "overcast",
    45: "foggy",
    48: "depositing rime fog",
    51: "light drizzle",
    53: "moderate drizzle",
    55: "dense drizzle",
    61: "slight rain",
    63: "moderate rain",
    65: "heavy rain",
    66: "light freezing rain",
    67: "heavy freezing rain",
    71: "slight snow",
    73: "moderate snow",
    75: "heavy snow",
    77: "snow grains",
    80: "slight rain showers",
    81: "moderate rain showers",
    82: "violent rain showers",
    85: "slight snow showers",
    86: "heavy snow showers",
    95: "thunderstorm",
    96: "thunderstorm with slight hail",
    99: "thunderstorm with heavy hail",
}

# Weather codes that indicate rain
RAIN_CODES = {51, 53, 55, 61, 63, 65, 66, 67, 80, 81, 82, 95, 96, 99}


def get_weather(city: str = DEFAULT_CITY) -> str:
    """
    Get current weather for a city.

    Args:
        city: City name (default: "New York")
              Supported cities: New York, London, Tokyo, San Francisco, Seattle

    Returns:
        A formatted string with the current weather conditions.
    """
    city = city.strip()
    today = date.today().isoformat()
    cache_key = city.lower().replace(" ", "_")
    cache_file = CACHE_DIR / f"weather_{cache_key}_{today}.json"

    # Check cache first
    if cache_file.exists():
        try:
            with open(cache_file) as f:
                data = json.load(f)
                return _format_weather_response(city, data)
        except (json.JSONDecodeError, KeyError):
            pass  # Cache corrupted, fetch fresh data

    # Get coordinates for the city
    coords = get_city_coordinates(city)
    if not coords:
        # City not in our list, use mock data
        data = get_mock_weather(city)
        return _format_weather_response(city, data) + f" (Note: {city} coordinates not found, using estimated data)"

    lat, lon = coords

    # Fetch from Open-Meteo API (no API key needed!)
    try:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,weather_code",
            "timezone": "auto",
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        result = response.json()
        current = result.get("current", {})

        data = {
            "temperature": current.get("temperature_2m", 20),
            "weather_code": current.get("weather_code", 0),
        }

        _save_to_cache(cache_file, data)
        return _format_weather_response(city, data)

    except requests.RequestException as e:
        # API error, fall back to mock data
        data = get_mock_weather(city)
        return _format_weather_response(city, data) + f" (fallback due to API error: {e})"


def _format_weather_response(city: str, data: dict) -> str:
    """Format weather data into a human-readable string."""
    temp = data.get("temperature", 20)
    weather_code = data.get("weather_code", 0)

    # Get condition from WMO code or use provided condition
    condition = data.get("condition") or WMO_CODES.get(weather_code, "unknown")

    # Check if it's rainy
    is_rainy = weather_code in RAIN_CODES or "rain" in condition.lower()

    if is_rainy:
        return f"The weather in {city} is rainy with a temperature of {temp:.0f}°C."
    else:
        return f"The weather in {city} is {condition} with a temperature of {temp:.0f}°C."


def _save_to_cache(cache_file: Path, data: dict) -> None:
    """Save data to cache file."""
    try:
        with open(cache_file, "w") as f:
            json.dump(data, f, indent=2)
    except IOError:
        pass  # Silently fail on cache write errors


if __name__ == "__main__":
    # Test the tool
    print(get_weather("New York"))
    print(get_weather("London"))
    print(get_weather("Tokyo"))
