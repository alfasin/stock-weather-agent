#!/usr/bin/env python3
"""
Stock Weather Agent - CLI Entry Point

Run the agent from the command line with a query.

Usage:
    python main.py "What's the outlook for AAPL?"
    python main.py "Check MSFT and the weather in New York"
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
        return

    query = " ".join(args)

    # Print config status
    print_config_status()
    print()

    # Import the agent
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
