#!/usr/bin/env python3
"""
Stock Weather Agent - CLI Entry Point

Run the agent from the command line with a query.

Usage:
    python main.py "What's the outlook for AAPL?"
    python main.py --solution "What's the outlook for NVDA in NYC?"
"""

import sys

from config import print_config_status


def main():
    # Parse arguments
    use_solution = "--solution" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--solution"]

    if not args or args[0] in ["-h", "--help"]:
        print(__doc__)
        print("\nOptions:")
        print("  --solution    Use the complete solution instead of assignments")
        print("\nExamples:")
        print('  python main.py "What\'s the outlook for AAPL?"')
        print('  python main.py "Check MSFT and the weather in New York"')
        print('  python main.py --solution "How is NVDA doing today?"')
        return

    query = " ".join(args)

    # Print config status
    print_config_status()
    print()

    # Import the appropriate agent
    if use_solution:
        print("Using: solutions/agent.py (complete reference)\n")
        from solutions.agent import run_agent
    else:
        print("Using: assignments/agent.py (student exercises)\n")
        from assignments.agent import run_agent

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
