"""transform.py - pure Python maths on the data. No network, no files."""
import statistics
from collections import Counter


def language_breakdown(repos, top_n=5):
    """Return [(language, count, percent), ...] for the top_n languages."""
    # repo.get("language") may be None (GitHub has no language for some repos)
    languages = [repo.get("language") or "Unknown" for repo in repos]
    total = len(languages)
    if total == 0:
        return []
    counts = Counter(languages)
    return [
        (lang, count, count / total * 100)
        for lang, count in counts.most_common(top_n)
    ]


def star_stats(repos):
    """Return (median, mean) of star counts."""
    stars = [repo.get("stargazers_count", 0) for repo in repos]
    if not stars:
        return 0, 0
    return statistics.median(stars), statistics.mean(stars)


def most_recently_updated(repos, n=10):
    """Return the n repos with the newest 'pushed_at' date."""
    # ISO dates like "2026-11-20T10:00:00Z" sort correctly as plain strings.
    return sorted(
        repos,
        key=lambda repo: repo.get("pushed_at") or "",
        reverse=True,
    )[:n]
