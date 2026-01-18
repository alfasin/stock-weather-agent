"""Mock data for offline/demo mode when API keys are not available."""

# Mock stock data - realistic responses for common tickers
MOCK_STOCK_DATA = {
    "AAPL": {
        "symbol": "AAPL",
        "name": "Apple Inc.",
        "price": 178.72,
        "changesPercentage": -0.45,
        "change": -0.81,
        "dayLow": 177.35,
        "dayHigh": 180.10,
        "volume": 52340000,
    },
    "MSFT": {
        "symbol": "MSFT",
        "name": "Microsoft Corporation",
        "price": 378.91,
        "changesPercentage": 0.32,
        "change": 1.21,
        "dayLow": 376.50,
        "dayHigh": 380.25,
        "volume": 18920000,
    },
    "NVDA": {
        "symbol": "NVDA",
        "name": "NVIDIA Corporation",
        "price": 142.50,
        "changesPercentage": -1.23,
        "change": -1.78,
        "dayLow": 140.80,
        "dayHigh": 145.20,
        "volume": 245000000,
    },
    "GOOGL": {
        "symbol": "GOOGL",
        "name": "Alphabet Inc.",
        "price": 175.23,
        "changesPercentage": 0.67,
        "change": 1.17,
        "dayLow": 173.80,
        "dayHigh": 176.50,
        "volume": 21500000,
    },
    "AMZN": {
        "symbol": "AMZN",
        "name": "Amazon.com Inc.",
        "price": 186.45,
        "changesPercentage": -0.89,
        "change": -1.68,
        "dayLow": 184.20,
        "dayHigh": 188.30,
        "volume": 35400000,
    },
    "TSLA": {
        "symbol": "TSLA",
        "name": "Tesla Inc.",
        "price": 248.50,
        "changesPercentage": 2.15,
        "change": 5.23,
        "dayLow": 242.10,
        "dayHigh": 251.80,
        "volume": 98700000,
    },
    "META": {
        "symbol": "META",
        "name": "Meta Platforms Inc.",
        "price": 505.75,
        "changesPercentage": -0.34,
        "change": -1.73,
        "dayLow": 502.30,
        "dayHigh": 510.20,
        "volume": 12300000,
    },
}

# Default mock response for unknown tickers
DEFAULT_MOCK_STOCK = {
    "price": 100.00,
    "changesPercentage": -0.50,
    "change": -0.50,
    "dayLow": 98.50,
    "dayHigh": 101.25,
    "volume": 1000000,
}

# Mock weather data for cities
MOCK_WEATHER_DATA = {
    "new york": {
        "temperature": 18,
        "weather_code": 61,  # Rain: Slight intensity
        "condition": "rainy",
    },
    "london": {
        "temperature": 12,
        "weather_code": 3,  # Overcast
        "condition": "cloudy",
    },
    "tokyo": {
        "temperature": 24,
        "weather_code": 0,  # Clear sky
        "condition": "sunny",
    },
    "san francisco": {
        "temperature": 16,
        "weather_code": 45,  # Fog
        "condition": "foggy",
    },
    "seattle": {
        "temperature": 14,
        "weather_code": 63,  # Rain: Moderate intensity
        "condition": "rainy",
    },
}

# Default mock weather for unknown cities
DEFAULT_MOCK_WEATHER = {
    "temperature": 20,
    "weather_code": 2,  # Partly cloudy
    "condition": "partly cloudy",
}


def get_mock_stock(ticker: str) -> dict:
    """Get mock stock data for a ticker."""
    ticker_upper = ticker.upper()
    if ticker_upper in MOCK_STOCK_DATA:
        return MOCK_STOCK_DATA[ticker_upper]
    # Return default with the requested ticker
    return {
        "symbol": ticker_upper,
        "name": f"{ticker_upper} Inc.",
        **DEFAULT_MOCK_STOCK,
    }


def get_mock_weather(city: str) -> dict:
    """Get mock weather data for a city."""
    city_lower = city.lower().strip()
    if city_lower in MOCK_WEATHER_DATA:
        return MOCK_WEATHER_DATA[city_lower]
    return {"city": city, **DEFAULT_MOCK_WEATHER}
