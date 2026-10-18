"""
update_readme.py
----------------
Fetches your GitHub repos and recent activity via the GitHub API,
then rewrites the dynamic sections in README.md between HTML comment markers.

Sections updated:
  - <!-- PROJECTS:START --> ... <!-- PROJECTS:END -->
  - <!-- ACTIVITY:START --> ... <!-- ACTIVITY:END -->
  - <!-- LAST_UPDATED:START --> ... <!-- LAST_UPDATED:END -->

Changes from the previous version:
  - Forks, archived repos and the profile repo itself are never listed.
  - Repos without a description show no empty "No description" line.
  - The public events API often omits PR/issue titles, so those lines fall
    back to the number ("PR #12") instead of printing an empty title.
  - A failed API call keeps the old section instead of breaking the run.
  - The timestamp only changes when the rest of the README changed, so the
    bot no longer commits every single day.
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

# Shown first, in this order. Forks and missing repos are skipped automatically.
PINNED_REPOS = [
    "Aegis",
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
    # A function replacement avoids backslash and group-reference surprises.
    return re.sub(
        pattern,
        lambda m: f"{m.group(1)}\n{new_body}\n{m.group(2)}",
        content,
        flags=re.DOTALL,
    )


def get_section(content: str, marker: str) -> str:
    m = re.search(rf"<!-- {marker}:START -->\n?(.*?)\n?<!-- {marker}:END -->", content, flags=re.DOTALL)
    return m.group(1) if m else ""


def clean(text: str, limit: int = 72) -> str:
    """One line, trimmed, with characters that break markdown italics/links removed."""
    text = (text or "").splitlines()[0] if text else ""
    return text[:limit].replace("_", " ").replace("`", "'").replace("[", "(").replace("]", ")")


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
        # The events API may leave out the commit list, so fall back to its size.
        commits = payload.get("commits") or []
        n = len(commits) or payload.get("distinct_size") or payload.get("size") or 0
        if not n:
            return None
        label = f"{n} commit{'s' if n > 1 else ''}"
        msg = clean(commits[-1].get("message", "")) if commits else ""
        tail = f" · _{msg}_" if msg else ""
        return f"🔨 Pushed **{label}** to [`{repo_name}`]({repo_url}){tail}"

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
        issue = payload.get("issue", {})
        number = issue.get("number")
        title = clean(issue.get("title", ""))
        url = issue.get("html_url") or (f"{repo_url}/issues/{number}" if number else repo_url)
        name = f"_{title}_" if title else (f"#{number}" if number else "")
        return f"🐛 {action.capitalize()} issue [{name}]({url}) in `{repo_name}`" if name else \
               f"🐛 {action.capitalize()} an issue in [`{repo_name}`]({repo_url})"

    if etype == "IssueCommentEvent":
        url = payload.get("comment", {}).get("html_url", repo_url)
        return f"💬 Commented on an issue in [`{repo_name}`]({url})"

    if etype == "PullRequestEvent":
        action = payload.get("action", "")
        pr = payload.get("pull_request", {})
        number = pr.get("number") or payload.get("number")
        title = clean(pr.get("title", ""))
        url = pr.get("html_url") or (f"{repo_url}/pull/{number}" if number else repo_url)
        if action == "closed" and pr.get("merged"):
            action = "merged"
        label = f"_{title}_" if title else (f"#{number}" if number else "")
        verb = action.capitalize()
        if label:
            return f"🔀 {verb} PR [{label}]({url}) in `{repo_name}`"
        return f"🔀 {verb} a pull request in [`{repo_name}`]({repo_url})"

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

def listable(repo: dict) -> bool:
    """Skip forks, archived repos, private repos and the profile repo itself."""
    return not (
        repo.get("fork")
        or repo.get("archived")
        or repo.get("private")
        or repo.get("name", "").lower() == GITHUB_USERNAME.lower()
    )


def build_projects_section(repos_raw: list) -> str:
    by_name = {r["name"]: r for r in repos_raw}

    lines = []
    shown = set()

    for name in PINNED_REPOS:
        repo = by_name.get(name)
        if repo and listable(repo):
            lines.append(format_repo(repo))
            shown.add(name)

    extras = sorted(
        [r for r in repos_raw if r["name"] not in shown and listable(r)],
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
    desc = (repo.get("description") or "").strip()
    url = repo.get("html_url", f"https://github.com/{GITHUB_USERNAME}/{name}")
    language = repo.get("language") or ""
    topics = repo.get("topics") or []
    emoji = repo_emoji(repo)

    tags = [f"`{t}`" for t in topics[:6]] if topics else ([f"`{language}`"] if language else [])

    lines = [f"### {emoji} [{name}]({url})"]
    if desc:
        lines.append(f"> {desc}")
    lines.append("")
    if tags:
        lines.append(" ".join(tags))
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


def build_activity_section(events: list) -> str:
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
        original = f.read()
    content = original

    # Each fetch is separate: if one fails, that section keeps its old text.
    try:
        print("  → Fetching repos...")
        repos_raw = gh_get(f"/users/{GITHUB_USERNAME}/repos?per_page=100&sort=updated")
        content = replace_section(content, "PROJECTS", build_projects_section(repos_raw))
    except (urllib.error.URLError, TimeoutError, KeyError) as e:
        print(f"  ! Could not update projects, keeping old section: {e}")

    try:
        print("  → Fetching recent activity...")
        events = gh_get(f"/users/{GITHUB_USERNAME}/events/public?per_page=30")
        content = replace_section(content, "ACTIVITY", build_activity_section(events))
    except (urllib.error.URLError, TimeoutError) as e:
        print(f"  ! Could not update activity, keeping old section: {e}")

    # Only bump the timestamp when something else actually changed.
    old_ts = get_section(original, "LAST_UPDATED").strip()
    if content != original or not old_ts:
        now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        content = replace_section(content, "LAST_UPDATED", now)
        print(f"  ✅ README updated at {now}")
    else:
        print("  = No changes, README left as is.")

    if content != original:
        with open(README_PATH, "w", encoding="utf-8") as f:
            f.write(content)


if __name__ == "__main__":
    main()
