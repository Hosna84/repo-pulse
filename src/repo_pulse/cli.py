"""cli.py - reads command-line options and connects the other modules."""
import argparse
import sys

from repo_pulse.fetch import FetchError, fetch_repositories
from repo_pulse.report import build_markdown, write_report
from repo_pulse.transform import language_breakdown, most_recently_updated, star_stats


def main():
    parser = argparse.ArgumentParser(description="When you wnat help")
    parser.add_argument("--topic", required=True, help="e.g. machine-learning")
    parser.add_argument("--min-stars", type=int, default=0, help="minimum stars")
    args = parser.parse_args()

    try:
        repos = fetch_repositories(args.topic, args.min_stars)
    except FetchError as err:
        print(f"Error: {err}", file=sys.stderr)
        sys.exit(1)

    if not repos:
        print("No repositories found. Try a different topic or lower --min-stars.")
        sys.exit(0)

    languages = language_breakdown(repos)
    median, mean = star_stats(repos)
    recent = most_recently_updated(repos)

    markdown = build_markdown(args.topic, args.min_stars, repos, languages, median, mean, recent)
    path = write_report(args.topic, markdown)
    print(f"Done! Analysed {len(repos)} repos. Report saved to {path}")

if __name__ == "__main__":
    main()
