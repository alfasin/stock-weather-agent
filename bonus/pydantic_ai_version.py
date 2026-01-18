"""
Stock Weather Agent - Pydantic AI Version

This shows how the same agent looks when built with a framework.
Compare this to the ~150 lines in agent.py!

The framework handles:
- Message history (memory)
- Tool execution loop
- Tool call parsing
- Error handling

Install: uv pip install pydantic-ai
Run: python bonus/pydantic_ai_version.py
"""

from pydantic_ai import Agent

from config import GROQ_API_KEY, GROQ_MODEL
from tools.stock_tool import get_stock_price
from tools.weather_tool import get_weather

# Check for API key
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not set! Add it to your .env file.")

# Create the agent with system prompt
agent = Agent(
    f"groq:{GROQ_MODEL}",
    system_prompt="""You are a financial analyst with an unusual theory:
you believe rainy weather correlates with lower stock performance.

When asked about stocks, you should:
1. Check the current weather conditions (especially if it's rainy)
2. Look up the stock price
3. Combine both pieces of information to make a prediction

Always be clear about the reasoning behind your predictions.
If it's rainy, you're more bearish. If it's sunny, you're more bullish.

Remember: This is a fun, educational example - not real financial advice!""",
)


# Register tools with decorators - that's it!
@agent.tool_plain
def check_stock_price(ticker: str) -> str:
    """Get the current stock price for a ticker symbol."""
    return get_stock_price(ticker)


@agent.tool_plain
def check_weather(city: str = "New York") -> str:
    """Get the current weather for a city."""
    return get_weather(city)


# The entire ReAct loop is handled by run_sync()!
if __name__ == "__main__":
    query = "What's the outlook for NVDA in New York today?"
    print(f"User: {query}\n")

    # This single line replaces the entire while loop!
    result = agent.run_sync(query)

    print(f"Agent: {result.output}")

    # You can also see the conversation history
    print("\n--- Message History ---")
    last = ''
    for msg in result.all_messages():
        print(f"{msg.kind}: {str(msg)[:100]}...")
        last = msg
    print("\n\nfinal response")
    print("==============")
    print(last.parts[0].content)
