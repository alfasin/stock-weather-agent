"""
Stock Weather Agent - Student Assignment

This file contains the skeleton for building a ReAct-style agent.
Complete the TODO exercises to make the agent work!

The agent combines stock data and weather forecasts to make predictions
based on the (fun) hypothesis that rainy days correlate with lower stock performance.
"""

import json
import time

import groq
from groq import Groq

from config import GROQ_API_KEY, GROQ_MODEL
from tools import TOOLS, TOOL_FUNCTIONS
from tools.stock_tool import get_stock_price
from tools.weather_tool import get_weather

# System prompt that defines the agent's personality and behavior
SYSTEM_PROMPT = """You are a financial analyst with an unusual theory: you believe rainy weather correlates with lower stock performance.

When asked about stocks, you should:
1. Check the current weather conditions (especially if it's rainy)
2. Look up the stock price
3. Combine both pieces of information to make a prediction

Always be clear about the reasoning behind your predictions. If it's rainy, you're more bearish. If it's sunny, you're more bullish.

Remember: This is a fun, educational example - not real financial advice!"""


def create_client() -> Groq:
    """Create a Groq client."""
    if not GROQ_API_KEY:
        raise ValueError(
            "GROQ_API_KEY not set! Please add it to your .env file.\n"
            "Get your key at: https://console.groq.com/"
        )

    return Groq(api_key=GROQ_API_KEY)


# Global client for retry function
_client = None


def get_client() -> Groq:
    """Get or create the global client."""
    global _client
    if _client is None:
        _client = create_client()
    return _client


def call_llm_with_retry(messages, tools, max_retries=3):
    """
    Call Groq API with retry logic for rate limiting.
    (Provided for you - handles rate limits)
    """
    client = get_client()
    for i in range(max_retries):
        try:
            return client.chat.completions.create(
                model=GROQ_MODEL,
                messages=messages,
                tools=tools,
            )
        except groq.RateLimitError:
            wait_time = (2 ** i) + 1  # Exponential backoff: 2s, 5s, 9s...
            print(f"Rate limit hit. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
    raise Exception("Max retries exceeded.")


def run_agent(user_query: str, max_iterations: int = 10) -> str:
    """
    Run the ReAct agent loop.

    This is the main agent loop that:
    1. Sends user query to the LLM
    2. Checks if LLM wants to use tools
    3. Executes tools and feeds results back
    4. Repeats until LLM gives a final answer

    Args:
        user_query: The user's question
        max_iterations: Maximum number of tool-calling iterations (safety limit)

    Returns:
        The agent's final response
    """
    # Initialize conversation with system prompt and user query
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_query},
    ]

    for iteration in range(max_iterations):
        print(f"\n--- Iteration {iteration + 1} ---")

        # Call the LLM (with retry for rate limiting)
        response = call_llm_with_retry(messages, TOOLS)

        msg = response.choices[0].message
        print(f"Assistant: {msg.content or '(calling tools...)'}")

        # ============================================================
        # TODO Exercise A: Add Memory (Message History)
        # ============================================================
        # The agent needs to "remember" what it said.
        # Append the assistant's response to the messages list.
        # This is critical - without this, the agent forgets everything!
        #
        # Hint: messages.append({"role": "assistant", ...})
        # You need to include both 'content' and 'tool_calls' if present.
        #
        # YOUR CODE HERE:
        pass  # Remove this and add your code
        # ============================================================

        # ============================================================
        # TODO Exercise B: Handle Tool Calls
        # ============================================================
        # Check if the LLM wants to call tools (msg.tool_calls).
        # If NO tool calls: the agent is done, return msg.content
        # If YES tool calls: execute each tool and continue the loop
        #
        # YOUR CODE HERE:
        pass  # Remove this and add your code
        # ============================================================

        # Process each tool call
        for tool_call in msg.tool_calls:
            fn_name = tool_call.function.name
            fn_args = json.loads(tool_call.function.arguments)

            print(f"  Tool call: {fn_name}({fn_args})")

            # ============================================================
            # TODO Exercise C: Handle Tool Hallucinations
            # ============================================================
            # Sometimes LLMs "hallucinate" tools that don't exist!
            # If fn_name is not in our TOOL_FUNCTIONS, we need to tell
            # the LLM that this tool doesn't exist.
            #
            # Current code will crash if the LLM calls a non-existent tool.
            # Fix it by returning an error message for unknown tools.
            #
            # YOUR CODE HERE (fix the else branch):
            if fn_name == "get_stock_price":
                observation = get_stock_price(fn_args.get("ticker", "AAPL"))
            elif fn_name == "get_weather":
                observation = get_weather(fn_args.get("city", "New York"))
            else:
                # 🚨 BUG: What happens if fn_name is "get_company_news"?
                # The LLM might hallucinate tools that don't exist!
                # Return an error message so the LLM knows to try something else.
                observation = "???"  # Fix this!
            # ============================================================

            print(f"  Result: {observation}")

            # Add the tool result to messages
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": observation,
            })

    # ============================================================
    # TODO Exercise D: Handle Memory Bloat
    # ============================================================
    # The messages list can grow very large over many iterations.
    # This can cause:
    # - Token limit exceeded errors
    # - Slower responses
    # - Higher API costs
    #
    # Implement a strategy to manage memory:
    # Option 1: Keep only the last N messages (simple)
    # Option 2: Summarize older messages (advanced)
    # Option 3: Keep system + user + last N assistant/tool messages
    #
    # Add your memory management code somewhere in this function!
    # ============================================================

    # ============================================================
    # TODO Exercise E: Handle Infinite Loops
    # ============================================================
    # Sometimes the LLM gets "stuck" calling the same tool repeatedly.
    # For example, it might keep calling get_stock_price("AAPL") forever.
    #
    # Implement loop detection:
    # 1. Track recent tool calls (name + args)
    # 2. If the same call appears 3+ times, break the loop
    # 3. Add a message nudging the LLM to give a final answer
    #
    # Add your loop detection code in this function!
    # ============================================================

    return "Max iterations reached. The agent couldn't complete the task."


if __name__ == "__main__":
    # Test the agent
    query = "What's the outlook for AAPL stock today?"
    print(f"User: {query}")
    response = run_agent(query)
    print(f"\nFinal Answer: {response}")
