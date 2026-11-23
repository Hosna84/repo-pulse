"""fetch.py - talks to the GitHub API. Nothing else lives here."""
import os

import httpx
from dotenv import load_dotenv

API_URL = "https://api.github.com/search/repositories"


class FetchError(Exception):
    """Our own error type, so the CLI can print a friendly message."""


def get_token():
    """Read the optional GITHUB_TOKEN from a local .env file / environment."""
    load_dotenv()  # copies lines from .env into the environment (does nothing if no .env)
    return os.getenv("GITHUB_TOKEN")  # None if it is not set


def fetch_repositories(topic, min_stars=0, limit=100):
    """Return a list of repo dicts for a topic, most-starred first."""
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "repo-pulse",
    }
    token = get_token()
    if token:
        headers["Authorization"] = f"Bearer {token}"

    params = {
        "q": f"topic:{topic} stars:>={min_stars}",
        "sort": "stars",
        "order": "desc",
        "per_page": min(limit, 100),  # GitHub allows at most 100 per page
    }

    try:
        response = httpx.get(API_URL, headers=headers, params=params, timeout=10.0)
    except httpx.TimeoutException:
        raise FetchError("The request timed out. Try again in a moment.")
    except httpx.RequestError as exc:  # no internet, DNS problem, etc.
        raise FetchError(f"Network problem: {exc}")

    if response.status_code in (403, 429):
        reset = response.headers.get("x-ratelimit-reset", "unknown")
        raise FetchError(
            f"Rate limited by GitHub (HTTP {response.status_code}). "
            f"Limit resets at unix time {reset}. "
            "Add a GITHUB_TOKEN to your .env file for a higher limit."
        )
    if response.status_code == 422:
        raise FetchError("GitHub rejected the search. Check the topic name.")
    if response.status_code != 200:
        raise FetchError(f"Unexpected response from GitHub: HTTP {response.status_code}")

    data = response.json()
    return data.get("items", [])  # .get() -> empty list instead of crashing
