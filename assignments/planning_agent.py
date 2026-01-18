"""
Stock Weather Agent - Planning Pattern (Student Assignment)

This file implements the "Plan-then-Execute" agent pattern.
Compare this to the ReAct pattern in agent.py to understand the differences!

PATTERN COMPARISON:
- ReAct:    Reason → Act → Observe → Reason → Act → Observe → Answer (interleaved)
- Planning: Plan all steps → Execute step 1 → Execute step 2 → ... → Answer (sequential)

The planning pattern is useful when:
- You know all required steps upfront
- Steps are independent (can be parallelized)
- You want faster execution (fewer LLM calls)
"""

import json
import time

import groq
from groq import Groq

from config import GROQ_API_KEY, GROQ_MODEL
from tools import TOOLS, TOOL_FUNCTIONS
from tools.stock_tool import get_stock_price
from tools.weather_tool import get_weather


# System prompt for the PLANNING phase
PLANNING_PROMPT = """You are a financial analyst assistant. When given a query, create a plan of tool calls needed to answer it.

Available tools:
- get_stock_price(ticker): Get current stock price and daily change
- get_weather(city): Get current weather conditions

Respond with a JSON array of tool calls in order. Example:
[
    {"tool": "get_weather", "args": {"city": "New York"}},
    {"tool": "get_stock_price", "args": {"ticker": "AAPL"}}
]

Only include tools that are necessary. If no tools are needed, respond with an empty array: []"""


# System prompt for the SYNTHESIS phase
SYNTHESIS_PROMPT = """You are a financial analyst with an unusual theory: you believe rainy weather correlates with lower stock performance.

Given the user's question and the tool results below, provide a helpful answer.
Combine the information to make predictions. If it's rainy, be more bearish. If it's sunny, be more bullish.

Remember: This is a fun, educational example - not real financial advice!"""


def create_client() -> Groq:
    """Create a Groq client."""
    if not GROQ_API_KEY:
        raise ValueError(
            "GROQ_API_KEY not set! Please add it to your .env file.\n"
            "Get your key at: https://console.groq.com/"
        )
    return Groq(api_key=GROQ_API_KEY)


_client = None


def get_client() -> Groq:
    """Get or create the global client."""
    global _client
    if _client is None:
        _client = create_client()
    return _client


def call_llm(messages, max_retries=3):
    """Call Groq API with retry logic for rate limiting."""
    client = get_client()
    for i in range(max_retries):
        try:
            return client.chat.completions.create(
                model=GROQ_MODEL,
                messages=messages,
            )
        except groq.RateLimitError:
            wait_time = (2 ** i) + 1
            print(f"Rate limit hit. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
    raise Exception("Max retries exceeded.")


def run_planning_agent(user_query: str) -> str:
    """
    Run the Planning agent (Plan-then-Execute pattern).

    Unlike ReAct which interleaves reasoning and action, this pattern:
    1. Creates a complete plan upfront
    2. Executes all steps sequentially (no LLM calls between steps)
    3. Synthesizes the final answer from all results

    Args:
        user_query: The user's question

    Returns:
        The agent's final response
    """

    # ================================================================
    # PHASE 1: PLANNING
    # ================================================================
    # Ask the LLM to create a plan (list of tool calls)
    # The LLM does NOT execute tools here - just plans what to do
    # ================================================================
    print("\n--- Phase 1: Planning ---")

    # ============================================================
    # TODO Exercise A: Create the Planning Request
    # ============================================================
    # Create a messages list with:
    # 1. System message using PLANNING_PROMPT
    # 2. User message with the query
    #
    # Then call the LLM and extract the plan from the response.
    #
    # Hint: The LLM will return a JSON array of tool calls.
    # You'll need to parse it with json.loads()
    #
    # YOUR CODE HERE:
    planning_messages = []  # Fix this!

    # Call LLM to get the plan
    # response = call_llm(planning_messages)
    # plan_text = response.choices[0].message.content

    plan = []  # This should be the parsed JSON array
    # ============================================================

    print(f"Plan: {json.dumps(plan, indent=2)}")

    # ================================================================
    # PHASE 2: EXECUTION
    # ================================================================
    # Execute each planned step sequentially.
    # NO reasoning between steps - just execute!
    # This is the key difference from ReAct.
    # ================================================================
    print("\n--- Phase 2: Execution ---")

    # ============================================================
    # TODO Exercise B: Execute the Plan
    # ============================================================
    # Loop through each step in the plan and execute the tool.
    # Store results in a list for the synthesis phase.
    #
    # Structure of each step: {"tool": "tool_name", "args": {...}}
    #
    # Handle these cases:
    # 1. Tool exists: execute it and store the result
    # 2. Tool doesn't exist: store an error message
    #
    # YOUR CODE HERE:
    results = []  # List of {"tool": ..., "args": ..., "result": ...}

    for step in plan:
        tool_name = step.get("tool")
        tool_args = step.get("args", {})

        print(f"  Executing: {tool_name}({tool_args})")

        # Execute the tool
        # Hint: Check if tool_name is in TOOL_FUNCTIONS
        # If yes: result = TOOL_FUNCTIONS[tool_name](**tool_args)
        # If no: result = f"Error: Unknown tool '{tool_name}'"

        result = "???"  # Fix this!

        print(f"  Result: {result}")
        results.append({
            "tool": tool_name,
            "args": tool_args,
            "result": result,
        })
    # ============================================================

    # ================================================================
    # PHASE 3: SYNTHESIS
    # ================================================================
    # Send all results to the LLM to generate the final answer.
    # The LLM combines all information into a coherent response.
    # ================================================================
    print("\n--- Phase 3: Synthesis ---")

    # ============================================================
    # TODO Exercise C: Synthesize the Final Answer
    # ============================================================
    # Create a messages list with:
    # 1. System message using SYNTHESIS_PROMPT
    # 2. User message containing:
    #    - The original query
    #    - All tool results (formatted nicely)
    #
    # Format suggestion for the user message:
    # """
    # User question: {user_query}
    #
    # Tool results:
    # - get_weather({"city": "New York"}): The weather in New York is rainy...
    # - get_stock_price({"ticker": "AAPL"}): Current price for AAPL...
    # """
    #
    # YOUR CODE HERE:
    synthesis_messages = []  # Fix this!

    # Call LLM to synthesize
    # response = call_llm(synthesis_messages)
    # final_answer = response.choices[0].message.content

    final_answer = "TODO: Implement synthesis phase"  # Fix this!
    # ============================================================

    return final_answer


if __name__ == "__main__":
    # Test the planning agent
    query = "What's the outlook for NVDA stock in NYC today?"
    print(f"User: {query}")
    response = run_planning_agent(query)
    print(f"\nFinal Answer: {response}")
