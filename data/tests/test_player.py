"""Quick test: look up an NBA player by name using the balldontlie API.

Usage:
    python data/tests/test_player.py                 # defaults to Jayson Tatum
    python data/tests/test_player.py "LeBron James"
"""

import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

BASE_URL = "https://api.balldontlie.io/v1"

# .env lives in the project root, three levels up from data/tests/
load_dotenv(Path(__file__).resolve().parents[2] / ".env")
API_KEY = os.getenv("BALLDONTLIE_API_KEY")


def search_player(name):
    """Return players matching a name. Full names are split into first/last."""
    parts = name.split()
    if len(parts) >= 2:
        params = {"first_name": parts[0], "last_name": " ".join(parts[1:])}
    else:
        params = {"search": name}

    response = requests.get(
        f"{BASE_URL}/players",
        headers={"Authorization": API_KEY},
        params=params,
        timeout=10,
    )
    response.raise_for_status()
    return response.json()["data"]


def main():
    if not API_KEY or API_KEY == "your_api_key_here":
        sys.exit("BALLDONTLIE_API_KEY is not set. Add your real key to .env first.")

    name = sys.argv[1] if len(sys.argv) > 1 else "Jayson Tatum"
    players = search_player(name)

    if not players:
        print(f"No players found for '{name}'.")
        return

    for p in players:
        team = p.get("team") or {}
        print(f"{p['first_name']} {p['last_name']} (id {p['id']})")
        print(f"  Team:     {team.get('full_name', 'N/A')}")
        print(f"  Position: {p.get('position') or 'N/A'}")
        print(f"  Height:   {p.get('height') or 'N/A'}")
        print(f"  Jersey:   {p.get('jersey_number') or 'N/A'}")


if __name__ == "__main__":
    main()
