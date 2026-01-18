# Mist-Clearing Cheat Sheet

## The "Magic" vs The "Reality"

This cheat sheet maps framework abstractions to their underlying implementations.
After building the agent from scratch, you'll understand what's really happening!

| Concept | Framework "Magic" | Raw SDK Reality |
|---------|-------------------|-----------------|
| **Memory** | `MemoryBuffer()`, `ConversationHistory` | A Python `list` of message dictionaries |
| **Reasoning** | `Agent.run()`, `ReActAgent` | A `while` loop asking the LLM "what next?" |
| **Acting** | `ToolAction()`, `@tool` decorator | An `if/elif/else` calling Python functions |
| **Observation** | `OutputParser`, tool result handling | Appending function return value to the list |
| **Loop Control** | `max_iterations` parameter | A `for` loop with a counter |
| **State** | `AgentState`, `RunContext` | Variables in your function scope |

## The ReAct Pattern Demystified

```
┌─────────────────────────────────────────────────┐
│                  ReAct Loop                      │
│                                                  │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐  │
│  │ Reasoning│───▶│  Action  │───▶│Observation│  │
│  │  (LLM)   │    │  (Tool)  │    │ (Result)  │  │
│  └──────────┘    └──────────┘    └──────────┘  │
│       ▲                               │         │
│       └───────────────────────────────┘         │
│                                                  │
│  Framework: agent.run()                          │
│  Reality:   while True: ...                      │
└─────────────────────────────────────────────────┘
```

## What Each Framework Component Does

### 1. Message History = A List

```python
# Framework way
memory = ConversationBufferMemory()
memory.add_message(...)

# Reality
messages = []
messages.append({"role": "assistant", "content": "..."})
```

### 2. Tool Execution = Function Calls

```python
# Framework way
@agent.tool
def get_weather(city: str) -> str:
    ...

# Reality
TOOL_FUNCTIONS = {"get_weather": get_weather}
result = TOOL_FUNCTIONS[tool_name](**args)
```

### 3. Agent Loop = While Loop

```python
# Framework way
result = agent.run(query)

# Reality
while True:
    response = client.chat.completions.create(...)
    if not response.tool_calls:
        return response.content
    # execute tools, append results
```

### 4. Tool Schema = JSON Dictionary

```python
# Framework way (inferred from type hints)
@agent.tool
def get_weather(city: str) -> str:
    """Get weather for a city."""
    ...

# Reality
{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get weather for a city.",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string"}
            }
        }
    }
}
```

## Why Use Frameworks Then?

After building it yourself, here's what frameworks actually provide:

| Benefit | Description |
|---------|-------------|
| **Less Boilerplate** | You wrote ~150 lines; framework does it in ~20 |
| **Type Safety** | Automatic schema generation from type hints |
| **Error Handling** | Built-in retry logic, rate limiting |
| **Streaming** | Complex async streaming handled for you |
| **Testing** | Mocking and testing utilities |
| **Multi-Model** | Easy switching between LLM providers |

## The Takeaway

> "Any sufficiently advanced technology is indistinguishable from magic."
> — Arthur C. Clarke

But now the magic is gone. You know:

1. **Memory** is just appending to a list
2. **Reasoning** is asking an LLM what to do next
3. **Action** is calling a Python function
4. **Observation** is putting the result back in the list
5. **The loop** continues until no more tools are called

Frameworks are convenience, not magic. Use them when they help, but understand what's underneath!
