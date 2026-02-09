# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Educational AI agent workshop. Students build a ReAct-style and a Planning-style agent from scratch that combines stock data and weather forecasts. The codebase is intentionally simple — files in `assignments/` contain TODO exercises for students to complete.

## Commands

```bash
# Install dependencies
uv sync

# Run the ReAct agent (default)
uv run python main.py "What's the outlook for AAPL?"

# Run the Planning agent
uv run python main.py --planning "What's the outlook for NVDA in NYC?"

# Test individual tools
uv run python tools/stock_tool.py
uv run python tools/weather_tool.py

# Run bonus framework comparison
uv pip install pydantic-ai
uv run python bonus/pydantic_ai_version.py
```

No test suite, linter, or CI/CD — this is a teaching project.

## Architecture

**Two agent patterns** in `assignments/`:
- **`react_agent.py`** — ReAct loop: interleaved LLM reasoning + tool execution. LLM decides next action after each observation. 5 student exercises (A–E).
- **`planning_agent.py`** — Plan-then-execute: LLM creates full plan upfront, tools run sequentially, LLM synthesizes final answer. 3 student exercises (A–C).

**Shared infrastructure:**
- `tools/__init__.py` — Tool registry using OpenAI function-calling JSON schema format. Maps tool names to functions via `TOOL_FUNCTIONS` dict.
- `tools/stock_tool.py` — Stock prices via Financial Modeling Prep API. Falls back to `mock_data.py` if `FMP_API_KEY` is missing.
- `tools/weather_tool.py` — Weather via Open-Meteo API (free, no key needed). Rain detection uses WMO weather codes (51–82, 95–99).
- `config.py` — Env var loading, model selection, city coordinate mapping, cache config.
- `mock_data.py` — Hardcoded fallback data for 8 tickers and 5 cities.
- `main.py` — CLI entry point, dispatches to ReAct or Planning agent based on `--planning` flag.

**External APIs:**
- **Groq** (LLM inference) — required, key in `.env`
- **FMP** (stock data) — optional, falls back to mock data
- **Open-Meteo** (weather) — free, no auth

**Caching:** API responses cached as JSON in `cache/` with 24-hour TTL (by date in filename).

## Key Conventions

- LLM calls use `call_llm_with_retry()` with exponential backoff for Groq rate limits.
- Default model: `llama-4-scout-17b-16e-instruct` (configurable via `GROQ_MODEL` env var).
- Tool definitions follow OpenAI function-calling format — see `TOOLS` list in `tools/__init__.py`.
- `assignments/` files have clearly marked `# TODO Exercise X:` blocks where student code goes. Preserve these markers and surrounding comments when editing.
