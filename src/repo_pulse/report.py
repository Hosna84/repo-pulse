"""report.py - turns the computed numbers into a Markdown file."""
from datetime import datetime, timezone
from pathlib import Path


def build_markdown(topic, min_stars, repos, languages, median, mean, recent):
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        f"# GitHub Topic Report: `{topic}`",
        "",
        f"_Generated: {now} | Minimum stars: {min_stars} | Repos analysed: {len(repos)}_",
        "",
        "## Top programming languages",
        "",
        "| Language | Repos | Share |",
        "|---|---:|---:|",
    ]
    for lang, count, pct in languages:
        lines.append(f"| {lang} | {count} | {pct:.1f}% |")

    skew = mean / median if median else 0
    lines += [
        "",
        "## Star counts: median vs mean",
        "",
        f"- **Median:** {median:,.0f}",
        f"- **Mean:** {mean:,.0f}",
        f"- The mean is **{skew:.1f}x** the median: a few mega-repositories "
        "pull the average up, so the median describes a 'typical' repo better.",
        "",
        "## 10 most recently updated repositories",
        "",
    ]
    for repo in recent:
        name = repo.get("full_name", "unknown")
        url = repo.get("html_url", "")
        stars = repo.get("stargazers_count", 0)
        pushed = (repo.get("pushed_at") or "n/a")[:10]
        lines.append(f"- [{name}]({url}) - ⭐ {stars:,} - updated {pushed}")

    return "\n".join(lines) + "\n"


def write_report(topic, markdown, out_dir="reports"):
    """Save to reports/<topic>-summary.md and a timestamped copy."""
    folder = Path(out_dir)
    folder.mkdir(exist_ok=True)  # create the folder if it is missing
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    path = folder / f"{topic}-summary-{stamp}.md"
    path.write_text(markdown, encoding="utf-8")
    return path
