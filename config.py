"""Configuration and environment settings for the stock-weather agent."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
FMP_API_KEY = os.getenv("FMP_API_KEY")

# Groq API settings
# Available models (see README for comparison):
# - meta-llama/llama-4-scout-17b-16e-instruct (default, best balance)
# - llama-3.1-8b-instant (highest rate limits, good for workshops)
# - llama-3.3-70b-versatile (smartest, but lowest rate limits)
GROQ_MODEL = os.getenv("GROQ_MODEL", "meta-llama/llama-4-scout-17b-16e-instruct")

# Mock mode detection
# - Groq: Required for the agent to work
# - FMP: Optional, falls back to mock data if missing
USE_MOCK_STOCK = not FMP_API_KEY
USE_MOCK_WEATHER = False  # Open-Meteo is free, no API key needed

# Default settings
DEFAULT_CITY = "New York"
CACHE_TTL_HOURS = 24

# Cache directory
CACHE_DIR = Path(__file__).parent / "cache"
CACHE_DIR.mkdir(exist_ok=True)

# City coordinates for weather lookups
CITY_COORDINATES = {
    "new york": {"lat": 40.7128, "lon": -74.0060},
    "london": {"lat": 51.5074, "lon": -0.1278},
    "tokyo": {"lat": 35.6762, "lon": 139.6503},
    "san francisco": {"lat": 37.7749, "lon": -122.4194},
    "seattle": {"lat": 47.6062, "lon": -122.3321},
}


def get_city_coordinates(city: str) -> tuple[float, float] | None:
    """Get latitude and longitude for a city name."""
    normalized = city.lower().strip()
    if normalized in CITY_COORDINATES:
        coords = CITY_COORDINATES[normalized]
        return coords["lat"], coords["lon"]
    return None


def print_config_status():
    """Print current configuration status for debugging."""
    print("=== Configuration Status ===")
    print(f"Groq API Key: {'✓ Set' if GROQ_API_KEY else '✗ Missing (required!)'}")
    print(f"FMP API Key: {'✓ Set' if FMP_API_KEY else '✗ Missing (using mock data)'}")
    print(f"Mock Stock Data: {'Yes' if USE_MOCK_STOCK else 'No'}")
    print(f"Cache Directory: {CACHE_DIR}")
    print("============================")


if __name__ == "__main__":
    print_config_status()
