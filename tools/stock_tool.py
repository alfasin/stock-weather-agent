"""Stock price tool using Financial Modeling Prep API with caching."""

import json
from datetime import date
from pathlib import Path

import requests

from config import CACHE_DIR, FMP_API_KEY, USE_MOCK_STOCK
from mock_data import get_mock_stock


def get_stock_price(ticker: str) -> str:
    """
    Get current stock price for a ticker symbol.

    Args:
        ticker: Stock ticker symbol (e.g., "AAPL", "MSFT")

    Returns:
        A formatted string with the current price and daily change.
    """
    ticker = ticker.upper().strip()
    today = date.today().isoformat()
    cache_file = CACHE_DIR / f"stock_{ticker}_{today}.json"

    # Check cache first
    if cache_file.exists():
        try:
            with open(cache_file) as f:
                data = json.load(f)
                return _format_stock_response(ticker, data)
        except (json.JSONDecodeError, KeyError):
            pass  # Cache corrupted, fetch fresh data

    # Use mock data if no API key
    if USE_MOCK_STOCK:
        data = get_mock_stock(ticker)
        _save_to_cache(cache_file, data)
        return _format_stock_response(ticker, data) + " (mock data)"

    # Fetch from FMP API
    try:
        url = "https://financialmodelingprep.com/stable/quote"
        params = {"symbol": ticker, "apikey": FMP_API_KEY}
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        result = response.json()
        if not result or len(result) == 0:
            # Ticker not found, use mock data
            data = get_mock_stock(ticker)
            return f"Ticker {ticker} not found. Using estimated data: " + _format_stock_response(ticker, data)

        data = result[0]
        _save_to_cache(cache_file, data)
        return _format_stock_response(ticker, data)

    except requests.RequestException as e:
        # API error, fall back to mock data
        data = get_mock_stock(ticker)
        return _format_stock_response(ticker, data) + f" (fallback due to API error: {e})"


def _format_stock_response(ticker: str, data: dict) -> str:
    """Format stock data into a human-readable string."""
    price = data.get("price", 0)
    change_pct = data.get("changesPercentage", 0)

    # Format the change direction
    direction = "+" if change_pct >= 0 else ""

    return f"Current price for {ticker}: ${price:.2f} ({direction}{change_pct:.2f}% change today)."


def _save_to_cache(cache_file: Path, data: dict) -> None:
    """Save data to cache file."""
    try:
        with open(cache_file, "w") as f:
            json.dump(data, f, indent=2)
    except IOError:
        pass  # Silently fail on cache write errors


if __name__ == "__main__":
    # Test the tool
    print(get_stock_price("AAPL"))
    print(get_stock_price("NVDA"))
    print(get_stock_price("MSFT"))
