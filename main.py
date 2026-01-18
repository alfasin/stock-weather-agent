#!/usr/bin/env python3
"""
Stock Weather Agent - CLI Entry Point

Run the agent from the command line with a query.

Usage:
    python main.py "What's the outlook for AAPL?"
    python main.py "Check MSFT and the weather in New York"
    python main.py --planning "What's the outlook for NVDA in NYC?"
"""

import sys

from config import print_config_status


def main():
    args = sys.argv[1:]

    if not args or args[0] in ["-h", "--help"]:
        print(__doc__)
        print("\nExamples:")
        print('  python main.py "What\'s the outlook for AAPL?"')
        print('  python main.py "Check MSFT and the weather in New York"')
        print('  python main.py --planning "What\'s the outlook for NVDA in NYC?"')
        print("\nFlags:")
        print("  --planning    Use the planning agent instead of ReAct")
        return

    # Check for --planning flag
    use_planning = "--planning" in args
    if use_planning:
        args = [a for a in args if a != "--planning"]

    query = " ".join(args)

    # Print config status
    print_config_status()
    print()

    # Import the appropriate agent
    if use_planning:
        from assignments.planning_agent import run_planning_agent as run_agent
        print("[Using Planning Agent]")
    else:
        from assignments.react_agent import run_agent
        print("[Using ReAct Agent]")

    # Run the agent
    print(f"User: {query}")
    print("=" * 50)

    try:
        response = run_agent(query)
        print("\n" + "=" * 50)
        print(f"Final Answer:\n{response}")
    except ValueError as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure you've set up your .env file with the required API keys.")
        print("See .env.example for the template.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        raise


if __name__ == "__main__":
    main()
