import os
import requests
import json
from datetime import datetime, timezone
from typing import List

USERNAME = "pinkycollie"
ORG_LIST = os.environ.get("ORG_LIST", "")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
API_URL = "https://api.github.com"

HEADERS = {"Accept": "application/vnd.github+json"}
if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"token {GITHUB_TOKEN}"

def get_repos_for_user(username: str) -> List[dict]:
    repos = []
    page = 1
    while True:
        res = requests.get(f"{API_URL}/users/{username}/repos?per_page=100&page={page}", headers=HEADERS)
        if res.status_code != 200:
            break
        batch = res.json()
        if not batch:
            break
        repos += batch
        page += 1
    return repos

def get_repos_for_org(org: str) -> List[dict]:
    repos = []
    page = 1
    while True:
        res = requests.get(f"{API_URL}/orgs/{org}/repos?per_page=100&page={page}", headers=HEADERS)
        if res.status_code != 200:
            break
        batch = res.json()
        if not batch:
            break
        repos += batch
        page += 1
    return repos

def get_latest_commit(owner, repo):
    res = requests.get(f"{API_URL}/repos/{owner}/{repo}/commits?per_page=1", headers=HEADERS)
    if res.status_code == 200:
        data = res.json()
        if data:
            return {
                "sha": data[0]["sha"],
                "date": data[0]["commit"]["committer"]["date"],
                "message": data[0]["commit"]["message"]
            }
    return None

def get_latest_release(owner, repo):
    res = requests.get(f"{API_URL}/repos/{owner}/{repo}/releases/latest", headers=HEADERS)
    if res.status_code == 200:
        data = res.json()
        return {
            "tag": data["tag_name"],
            "published_at": data["published_at"],
            "url": data["html_url"],
        }
    return None

def get_open_issues(owner, repo):
    res = requests.get(f"{API_URL}/repos/{owner}/{repo}", headers=HEADERS)
    if res.status_code == 200:
        data = res.json()
        return data.get("open_issues_count", 0)
    return 0

def get_open_pull_requests(owner, repo):
    res = requests.get(f"{API_URL}/repos/{owner}/{repo}/pulls?state=open&per_page=1", headers=HEADERS)
    if 'Link' in res.headers:
        import re
        m = re.search(r'&page=(\d+)>;\s*rel="last"', res.headers['Link'])
        if m:
            return int(m.group(1))
    if res.status_code == 200:
        return len(res.json())
    return 0

def collect_updates():
    site_updates = []
    seen = set()
    # User repos
    for repo in get_repos_for_user(USERNAME):
        full = repo['full_name']
        if full in seen:
            continue
        seen.add(full)
        repo_owner, repo_name = repo['owner']['login'], repo['name']
        info = {
            "repo": full,
            "url": repo['html_url'],
            "description": repo.get('description') or '',
            "updated_at": repo['updated_at'],
            "open_issues": get_open_issues(repo_owner, repo_name),
            "open_prs": get_open_pull_requests(repo_owner, repo_name),
            "latest_commit": get_latest_commit(repo_owner, repo_name),
            "latest_release": get_latest_release(repo_owner, repo_name),
            "private": repo['private'],
            "is_org": False,
        }
        site_updates.append(info)
    # Orgs
    for org in filter(None, [s.strip() for s in ORG_LIST.split(',')]):
        for repo in get_repos_for_org(org):
            full = repo['full_name']
            if full in seen:
                continue
            seen.add(full)
            repo_owner, repo_name = repo['owner']['login'], repo['name']
            info = {
                "repo": full,
                "url": repo['html_url'],
                "description": repo.get('description') or '',
                "updated_at": repo['updated_at'],
                "open_issues": get_open_issues(repo_owner, repo_name),
                "open_prs": get_open_pull_requests(repo_owner, repo_name),
                "latest_commit": get_latest_commit(repo_owner, repo_name),
                "latest_release": get_latest_release(repo_owner, repo_name),
                "private": repo['private'],
                "is_org": True,
                "org": org,
            }
            site_updates.append(info)
    return site_updates

def write_json(updates: list):
    os.makedirs("site", exist_ok=True)
    with open("site/updates.json", "w") as f:
        json.dump({"updated": datetime.now(timezone.utc).isoformat(), "repos": updates}, f, indent=2)

def render_site(updates: list):
    # Minimal HTML output; improve as needed!
    lines = [
        "<!DOCTYPE html>",
        "<html lang='en'>",
        "<head>",
        "  <meta charset='utf-8'>",
        "  <title>Project Updates</title>",
        "  <meta name='viewport' content='width=device-width,initial-scale=1'>",
        "  <style>body{font:1.1em sans-serif;max-width:44em;margin:auto;}a{color:#1a0dab}h1{margin-top:2em;}h2{border-bottom:1px solid #ccc;}code{background:#f7f7f7;padding:0.1em 0.4em;border-radius:3px;}</style>",
        "</head>",
        "<body>",
        "<a href='#content' class='skip-link'>Skip to content</a>",
        "<main id='content'>",
        "<h1>Recent Project Updates</h1>",
        "<p>Generated: " + datetime.now(timezone.utc).isoformat() + " UTC</p>",
        "<ul>",
    ]
    for upd in updates:
        lines.append(f"<li><a href='{upd['url']}'>{upd['repo']}</a> &mdash; {upd.get('description','')}")
        lines.append("<ul>")
        if upd["latest_release"]:
            lines.append(f"<li><strong>Latest Release:</strong> <a href='{upd['latest_release']['url']}'>{upd['latest_release']['tag']}</a> ({upd['latest_release']['published_at'][:10]})</li>")
        if upd["latest_commit"]:
            msg = upd['latest_commit']['message'].splitlines()[0]
            lines.append(f"<li><strong>Latest Commit:</strong> {upd['latest_commit']['date'][:10]} - <code>{msg}</code></li>")
        lines.append(f"<li><strong>Open Issues:</strong> {upd['open_issues']} | <strong>Open PRs:</strong> {upd['open_prs']}</li>")
        lines.append("</ul>")
        lines.append("</li>")
    lines.extend(["</ul>", "<p><small>(c) pinkycollie</small></p>", "</main>", "</body></html>"])
    with open("site/index.html", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

def main():
    updates = collect_updates()
    write_json(updates)
    render_site(updates)

if __name__ == "__main__":
    main()