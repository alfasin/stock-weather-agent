"""Tool definitions and registry for the stock-weather agent."""

from tools.stock_tool import get_stock_price
from tools.weather_tool import get_weather

# OpenAI-format tool definitions
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_stock_price",
            "description": "Get the current stock price and daily change for a given ticker symbol. Use this to look up stock information for companies.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {
                        "type": "string",
                        "description": "The stock ticker symbol (e.g., 'AAPL' for Apple, 'MSFT' for Microsoft, 'NVDA' for NVIDIA)",
                    }
                },
                "required": ["ticker"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather conditions for a city. Useful for checking if it's rainy, which may affect stock performance predictions.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The city name (e.g., 'New York', 'London', 'Tokyo'). Defaults to 'New York' if not specified.",
                        "default": "New York",
                    }
                },
                "required": [],
            },
        },
    },
]

# Map function names to their implementations
TOOL_FUNCTIONS = {
    "get_stock_price": get_stock_price,
    "get_weather": get_weather,
}

__all__ = ["TOOLS", "TOOL_FUNCTIONS", "get_stock_price", "get_weather"]
