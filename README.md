# Rainy Day Stock Agent

A workshop project demonstrating AI agents with tool use. Build a ReAct-style agent from scratch that combines stock market data and weather forecasts to make predictions based on the (fun) hypothesis that rainy days correlate with lower stock performance.

## What Makes a System "Agentic"?

An **agent** is more than a chatbot. It has:

| Chatbot | Agent |
|---------|-------|
| Responds to one message | Runs autonomously until task is done |
| No tools | Uses tools (APIs, functions, databases) |
| Stateless | Maintains memory across turns |
| Single response | Loops: Reason → Act → Observe → Repeat |

### The Agent Loop

```
User Query
    ↓
┌─────────────────────────┐
│  1. PERCEIVE            │  ← Read input/observations
│  2. REASON              │  ← Decide what to do next
│  3. ACT                 │  ← Call a tool or respond
│  4. OBSERVE             │  ← Get tool result
│  └──→ Loop until done   │
└─────────────────────────┘
    ↓
Final Answer
```

## What You'll Learn

- How AI agents work under the hood (the ReAct loop)
- Tool/function calling with LLMs
- Message history management (agent "memory")
- Handling edge cases: hallucinations, loops, memory bloat
- How frameworks abstract these patterns

## Tech Stack

- **LLM**: Groq (free tier, very fast inference)
- **Stock Data**: Financial Modeling Prep (FMP) API
- **Weather Data**: Open-Meteo API (free, no API key required)
- **Language**: Python with `groq` SDK

## Quick Start

### 1. Clone and Install

```bash
cd stock-weather-agent
uv sync
```

### 2. Get API Keys

You need **two API keys** (one is optional):

| API | Required? | Get it at |
|-----|-----------|-----------|
| Groq | Yes | https://console.groq.com/ |
| Financial Modeling Prep | Optional* | https://site.financialmodelingprep.com/developer/docs |

*Stock data falls back to mock data if FMP key is missing.

Weather API (Open-Meteo) requires **no API key** - it's completely free!

### Model Selection

You can choose between three Groq models by setting `GROQ_MODEL` in your `.env`:

| Model | Best For | Rate Limits |
|-------|----------|-------------|
| `meta-llama/llama-4-scout-17b-16e-instruct` | **Default** - Best balance of speed and quality | 30K TPM, 500K TPD |
| `llama-3.1-8b-instant` | Workshops with many students (highest limits) | 14.4K RPD, 500K TPD |
| `llama-3.3-70b-versatile` | Best reasoning (but lower limits) | 1K RPD, 100K TPD |

*TPM = Tokens Per Minute, TPD = Tokens Per Day, RPD = Requests Per Day*

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env and add your API keys
```

### 4. Run the Agent

#### Option A: Using `uv run` (recommended)

`uv` automatically manages the virtual environment - no activation needed:

```bash
uv run python main.py "What's the outlook for AAPL?"
```

#### Option B: Activate venv manually

If you prefer to activate the virtual environment yourself:

```bash
# macOS/Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate

# Now run directly without 'uv run'
python main.py "What's the outlook for AAPL?"
```

## Workshop Exercises

This workshop includes two agent patterns to implement. Each teaches different concepts about how AI agents work.

### ReAct Agent Exercises

Open `assignments/react_agent.py` and complete the TODO exercises:

**Learning goals:** Dynamic reasoning, tool calling, memory management, error handling

| Exercise | Topic | Description |
|----------|-------|-------------|
| **A** | Memory | The agent needs to remember what it said. Without message history, it forgets everything! |
| **B** | Tool Calls | Implement the logic to detect when the LLM wants to call tools vs. give a final answer. |
| **C** | Hallucinations | LLMs sometimes "hallucinate" tools that don't exist. Handle this gracefully. |
| **D** | Memory Bloat | The message list can grow too large. Implement a strategy to manage it. |
| **E** | Infinite Loops | Detect when the agent is stuck calling the same tool repeatedly. |

### Planning Agent Exercises

Open `assignments/planning_agent.py` and complete the TODO exercises:

**Learning goals:** Upfront planning, sequential execution, result synthesis

| Exercise | Topic | Description |
|----------|-------|-------------|
| **A** | Create the Plan | Build the planning phase prompt and parse the LLM's JSON plan response. |
| **B** | Execute the Plan | Loop through each planned tool call and execute it, handling unknown tools. |
| **C** | Synthesize Results | Combine all tool results into a coherent final answer for the user. |

## Agent Patterns Comparison

This workshop includes two agent patterns. Try the same query with both to see the difference!

**Query:** "What's the outlook for NVDA in NYC?"

| Pattern | Flow |
|---------|------|
| **ReAct** | Reason("need weather") → get_weather() → Reason("need stock") → get_stock() → Answer |
| **Planning** | Plan(["get_weather", "get_stock"]) → Execute all → Answer |
| **Framework** | Same as ReAct, but abstracted by pydantic-ai |

### Running Each Pattern

```bash
# ReAct agent (default) - interleaved reasoning
uv run python main.py "What's the outlook for NVDA in NYC?"

# Planning agent - plan first, then execute all
uv run python main.py --planning "What's the outlook for NVDA in NYC?"
```

### When to Use Each Pattern

| Pattern | Best For |
|---------|----------|
| **ReAct** | Dynamic tasks where next step depends on previous results |
| **Planning** | Tasks with known steps that can be planned upfront |

## Project Structure

```
stock-weather-agent/
├── tools/
│   ├── __init__.py          # Tool registry and definitions
│   ├── stock_tool.py        # get_stock_price() with caching
│   └── weather_tool.py      # get_weather() with caching
├── assignments/
│   ├── react_agent.py       # ReAct pattern - complete the TODOs!
│   └── planning_agent.py    # Planning pattern - alternative approach
├── bonus/
│   ├── pydantic_ai_version.py  # Same agent in ~20 lines
│   └── cheat_sheet.md       # Framework "magic" explained
├── cache/                   # Cached API responses
├── config.py                # Configuration and API keys
├── mock_data.py             # Fallback data for offline mode
├── main.py                  # CLI entry point
├── .env.example             # Template for API keys
└── pyproject.toml           # Dependencies
```

## How It Works

### The ReAct Loop

```
User Query
    │
    ▼
┌─────────────────────────────────────┐
│           ReAct Loop                │
│                                     │
│  1. Send messages to LLM            │
│  2. LLM responds with:              │
│     - Tool calls → Execute tools    │
│     - Final answer → Return it      │
│  3. Add results to message history  │
│  4. Repeat until done               │
│                                     │
└─────────────────────────────────────┘
    │
    ▼
Final Answer
```

### The Tools

**get_stock_price(ticker)**
- Fetches current price and daily change from FMP API
- Caches responses for 24 hours
- Falls back to mock data if API unavailable

**get_weather(city)**
- Fetches current weather from Open-Meteo API
- Detects rain using WMO weather codes
- Supports: New York, London, Tokyo, San Francisco, Seattle

## Testing

### Without API Keys (Mock Mode)

```bash
uv run python main.py "What's the outlook for AAPL?"
```

Works with realistic mock data, showing the full ReAct loop.

### With API Keys

```bash
# Set keys in .env, then:
uv run python main.py "What's the outlook for NVDA?"
```

Verify real API calls by checking the `cache/` directory.

### Full Agent Test

```bash
uv run python main.py "I'm looking at MSFT stock. Check the weather in New York and tell me what you think will happen this week."
```

Once you complete the exercises, the agent should:
1. Call `get_weather("New York")`
2. Call `get_stock_price("MSFT")`
3. Combine both to make a prediction

## Bonus: Framework Comparison

After completing the exercises, check out `bonus/pydantic_ai_version.py` to see how frameworks abstract all this work:

```python
from pydantic_ai import Agent

agent = Agent('groq:llama-3.1-8b-instant', system_prompt="...")

@agent.tool
def get_weather(ctx, city: str):
    return "It is raining in NYC."

# The entire ReAct loop in one line!
result = agent.run_sync("How is NVDA doing?")
```

The ~150 lines you wrote is exactly what `agent.run_sync()` does internally. Now you understand what's under the hood!

See `bonus/cheat_sheet.md` for a full mapping of framework concepts to their raw implementations.

## License

MIT - Use this for your own workshops!
