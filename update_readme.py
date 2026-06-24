"""
update_readme.py
----------------
Fetches your GitHub repos and recent commits via the GitHub API,
then rewrites the dynamic sections in README.md between HTML comment markers.

Sections updated:
  - <!-- PROJECTS:START --> ... <!-- PROJECTS:END -->
  - <!-- ACTIVITY:START --> ... <!-- ACTIVITY:END -->
  - <!-- LAST_UPDATED:START --> ... <!-- LAST_UPDATED:END -->
"""

import os
import re
import json
import urllib.request
import urllib.error
from datetime import datetime, timezone

# ── config ────────────────────────────────────────────────────────────────────

GITHUB_USERNAME = "antonysabu1"
README_PATH = "README.md"

PINNED_REPOS = [
    "Aegis",
    "Relayboy",
    "ssh-attack-monitoring-using-splunk",
]

MAX_EXTRA_REPOS = 3
MAX_ACTIVITY = 7

# ── helpers ───────────────────────────────────────────────────────────────────

TOKEN = os.environ.get("GITHUB_TOKEN", "")


def gh_get(path: str) -> list | dict:
    url = f"https://api.github.com{path}"
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    if TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode())


def replace_section(content: str, marker: str, new_body: str) -> str:
    pattern = rf"(<!-- {marker}:START -->).*?(<!-- {marker}:END -->)"
    replacement = rf"\g<1>\n{new_body}\n\g<2>"
    return re.sub(pattern, replacement, content, flags=re.DOTALL)


# ── emoji heuristics ──────────────────────────────────────────────────────────

TOPIC_EMOJI = {
    "security": "🔐", "cryptography": "🔑", "network": "📡",
    "web": "🌐", "phishing": "🎣", "malware": "🦠", "python": "🐍",
    "flask": "⚗️", "linux": "🐧", "api": "🔌", "ctf": "🏴",
    "geolocation": "📍", "automation": "⚙️", "machine-learning": "🤖",
    "cli": "💻", "monitoring": "👁️", "detection": "🛡️", "splunk": "🖥️",
    "siem": "🖥️", "ssh": "🔒", "relay": "🔀", "defense": "🛡️",
}

DEFAULT_EMOJI = "🚀"


def repo_emoji(repo: dict) -> str:
    topics = repo.get("topics") or []
    name = (repo.get("name") or "").lower()
    desc = (repo.get("description") or "").lower()
    combined = " ".join(topics) + " " + name + " " + desc
    for keyword, emoji in TOPIC_EMOJI.items():
        if keyword in combined:
            return emoji
    return DEFAULT_EMOJI


# ── event formatting ──────────────────────────────────────────────────────────

def format_event(event: dict) -> str | None:
    etype = event.get("type", "")
    repo_name = event.get("repo", {}).get("name", "unknown/repo")
    repo_url = f"https://github.com/{repo_name}"
    payload = event.get("payload", {})

    if etype == "PushEvent":
        commits = payload.get("commits", [])
        if not commits:
            return None
        n = len(commits)
        msg = commits[-1].get("message", "").splitlines()[0][:72]
        label = f"{n} commit{'s' if n > 1 else ''}"
        return f"🔨 Pushed **{label}** to [`{repo_name}`]({repo_url}) — _{msg}_"

    if etype == "CreateEvent":
        ref_type = payload.get("ref_type", "")
        ref = payload.get("ref", "")
        if ref_type == "repository":
            return f"🆕 Created repository [`{repo_name}`]({repo_url})"
        if ref_type == "branch":
            return f"🌿 Created branch `{ref}` in [`{repo_name}`]({repo_url})"
        if ref_type == "tag":
            return f"🏷️ Tagged `{ref}` in [`{repo_name}`]({repo_url})"

    if etype == "IssuesEvent":
        action = payload.get("action", "")
        title = payload.get("issue", {}).get("title", "")[:72]
        url = payload.get("issue", {}).get("html_url", repo_url)
        return f"🐛 {action.capitalize()} issue [_{title}_]({url}) in `{repo_name}`"

    if etype == "IssueCommentEvent":
        url = payload.get("comment", {}).get("html_url", repo_url)
        return f"💬 Commented on an issue in [`{repo_name}`]({url})"

    if etype == "PullRequestEvent":
        action = payload.get("action", "")
        pr = payload.get("pull_request", {})
        title = pr.get("title", "")[:72]
        url = pr.get("html_url", repo_url)
        return f"🔀 {action.capitalize()} PR [_{title}_]({url}) in `{repo_name}`"

    if etype == "WatchEvent":
        return f"⭐ Starred [`{repo_name}`]({repo_url})"

    if etype == "ForkEvent":
        forkee = payload.get("forkee", {}).get("full_name", repo_name)
        return f"🍴 Forked [`{repo_name}`]({repo_url}) → `{forkee}`"

    if etype == "ReleaseEvent":
        tag = payload.get("release", {}).get("tag_name", "")
        url = payload.get("release", {}).get("html_url", repo_url)
        return f"🚢 Released [`{tag}`]({url}) in `{repo_name}`"

    return None


# ── build sections ────────────────────────────────────────────────────────────

def build_projects_section() -> str:
    repos_raw = gh_get(f"/users/{GITHUB_USERNAME}/repos?per_page=100&sort=updated")
    by_name = {r["name"]: r for r in repos_raw}

    lines = []
    shown = set()

    for name in PINNED_REPOS:
        repo = by_name.get(name)
        if repo:
            lines.append(format_repo(repo))
            shown.add(name)

    extras = sorted(
        [r for r in repos_raw if r["name"] not in shown and not r.get("fork") and not r.get("private")],
        key=lambda r: r.get("stargazers_count", 0),
        reverse=True,
    )[:MAX_EXTRA_REPOS]

    if extras:
        lines.append("\n### 🗂️ More Projects\n")
        for repo in extras:
            lines.append(format_repo_compact(repo))

    return "\n".join(lines)


def format_repo(repo: dict) -> str:
    name = repo.get("name", "")
    desc = repo.get("description") or "No description provided."
    url = repo.get("html_url", f"https://github.com/{GITHUB_USERNAME}/{name}")
    language = repo.get("language") or ""
    topics = repo.get("topics") or []
    emoji = repo_emoji(repo)

    tags = [f"`{t}`" for t in topics[:6]] if topics else ([f"`{language}`"] if language else [])

    lines = [
        f"### {emoji} [{name}]({url})",
        f"> {desc}",
        "",
    ]
    if tags:
        lines.append(" ".join(tags))
    lines.append(
        f"\n![Stars](https://img.shields.io/github/stars/{GITHUB_USERNAME}/{name}?style=flat-square&color=2e5d8e) "
        f"![Forks](https://img.shields.io/github/forks/{GITHUB_USERNAME}/{name}?style=flat-square&color=4a86c8)"
    )
    lines.append("\n---")
    return "\n".join(lines)


def format_repo_compact(repo: dict) -> str:
    name = repo.get("name", "")
    desc = (repo.get("description") or "").strip()
    url = repo.get("html_url", f"https://github.com/{GITHUB_USERNAME}/{name}")
    stars = repo.get("stargazers_count", 0)
    emoji = repo_emoji(repo)
    star_badge = f" ⭐ {stars}" if stars else ""
    desc_part = f" — {desc}" if desc else ""
    return f"- {emoji} [{name}]({url}){desc_part}{star_badge}"


def build_activity_section() -> str:
    try:
        events = gh_get(f"/users/{GITHUB_USERNAME}/events/public?per_page=30")
    except urllib.error.HTTPError:
        return "_Could not fetch recent activity._"

    lines = []
    for event in events:
        if len(lines) >= MAX_ACTIVITY:
            break
        formatted = format_event(event)
        if formatted:
            ts = event.get("created_at", "")
            try:
                dt = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
                date_str = dt.strftime("%b %d, %Y")
            except ValueError:
                date_str = ""
            suffix = f" <sub>{date_str}</sub>" if date_str else ""
            lines.append(f"{formatted}{suffix}")

    if not lines:
        return "_No public activity yet._"

    return "\n".join(f"{i + 1}. {line}" for i, line in enumerate(lines))


# ── main ──────────────────────────────────────────────────────────────────────

def main():
    print(f"Updating README for @{GITHUB_USERNAME}...")

    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    print("  → Fetching repos...")
    projects_md = build_projects_section()
    content = replace_section(content, "PROJECTS", projects_md)

    print("  → Fetching recent activity...")
    activity_md = build_activity_section()
    content = replace_section(content, "ACTIVITY", activity_md)

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    content = replace_section(content, "LAST_UPDATED", now)

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"  ✅ README updated at {now}")


if __name__ == "__main__":
    main()
