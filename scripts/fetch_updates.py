import os, json, shutil
from datetime import datetime, timezone
from typing import List
import requests

MAIN_USER = os.environ.get("MAIN_USER", "pinkycollie")
ORG_LIST = os.environ.get("ORG_LIST", "MBTQ-dev,PinkSync,VR4DEAF")
OFFICIAL_ORG = os.environ.get("OFFICIAL_ORG", "PinkSync")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
API_URL = "https://api.github.com"
HEADERS = {"Accept": "application/vnd.github+json"}
if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"token {GITHUB_TOKEN}"

# Fallback data for the ecosystem to ensure the portfolio is never empty
FALLBACK_REPOS = [
    {
        "repo": "DeafAUTH",
        "full_name": "PinkSync/DeafAUTH",
        "url": "https://github.com/PinkSync/DeafAUTH",
        "description": "Deaf-first identity and authentication — a passport, accessibility profile, and compliance key for Deaf professionals.",
        "open_issues": 2,
        "open_prs": 1,
        "latest_commit": {"date": "2024-11-28T14:30:00Z"},
        "category": "Core Identity",
        "status": "official"
    },
    {
        "repo": "PinkSync",
        "full_name": "PinkSync/PinkSync-Core",
        "url": "https://github.com/PinkSync/PinkSync-Core",
        "description": "Accessibility broker that coordinates speech, text, and sign language services in real-time.",
        "open_issues": 5,
        "open_prs": 0,
        "latest_commit": {"date": "2024-11-30T09:15:00Z"},
        "category": "Accessibility Tools",
        "status": "official"
    },
    {
        "repo": "360Magicians",
        "full_name": "MBTQ-dev/360Magicians",
        "url": "https://github.com/MBTQ-dev/360Magicians",
        "description": "Business lifecycle agents for Deaf founders — from idea intake to compliance and managed operations.",
        "open_issues": 0,
        "open_prs": 2,
        "latest_commit": {"date": "2024-11-25T16:45:00Z"},
        "category": "Business Magicians",
        "status": "personal"
    },
    {
        "repo": "FibonRose",
        "full_name": "pinkycollie/FibonRose",
        "url": "https://github.com/pinkycollie/FibonRose",
        "description": "The golden ratio applied to Deaf-first UI/UX systems and financial growth patterns.",
        "open_issues": 1,
        "open_prs": 0,
        "latest_commit": {"date": "2024-12-01T11:00:00Z"},
        "category": "Core Identity",
        "status": "personal"
    }
]

def get_repositories(user_or_org: str, entity_type: str = "user") -> List[dict]:
    repos = []
    url_type = "users" if entity_type == "user" else "orgs"
    page = 1
    while True:
        url = f"{API_URL}/{url_type}/{user_or_org}/repos?type=all&per_page=100&page={page}"
        try:
            r = requests.get(url, headers=HEADERS, timeout=10)
            if r.status_code != 200:
                print(f"Failed to fetch repos for {user_or_org}: {r.status_code}")
                break
            batch = r.json()
            if not batch: break
            repos += batch
            page += 1
        except Exception as e:
            print(f"Error fetching repos for {user_or_org}: {e}")
            break
    return repos

def get_latest_commit(o, r):
    try:
        res = requests.get(f"{API_URL}/repos/{o}/{r}/commits?per_page=1", headers=HEADERS, timeout=10)
        if res.status_code == 200 and res.json():
            d = res.json()[0]
            return {"sha": d["sha"], "date": d["commit"]["committer"]["date"], "message": d["commit"]["message"]}
    except: pass
    return None

def get_latest_release(o, r):
    try:
        res = requests.get(f"{API_URL}/repos/{o}/{r}/releases/latest", headers=HEADERS, timeout=10)
        if res.status_code == 200:
            d = res.json()
            return {"tag": d["tag_name"], "published_at": d["published_at"], "url": d["html_url"]}
    except: pass
    return None

def get_open_issues(o, r):
    try:
        res = requests.get(f"{API_URL}/repos/{o}/{r}", headers=HEADERS, timeout=10)
        if res.status_code == 200:
            j = res.json()
            return j.get("open_issues_count", 0)
    except: pass
    return 0

def get_open_pull_requests(o, r):
    try:
        res = requests.get(f"{API_URL}/repos/{o}/{r}/pulls?per_page=1&state=open", headers=HEADERS, timeout=10)
        if 'Link' in res.headers:
            import re
            m = re.search(r'&page=(\d+)>;\s*rel="last"', res.headers['Link'])
            if m:
                return int(m.group(1))
        if res.status_code == 200:
            return len(res.json())
    except: pass
    return 0

def classify_repo(repo, official_org):
    owner = repo['owner']['login']
    if owner.lower() == official_org.lower():
        return "official"
    if repo.get("fork"):
        return "fork"
    return "personal"

def categorize_repo(repo):
    name = repo.get("name", "").lower()
    desc = (repo.get("description") or "").lower()

    if any(k in name or k in desc for k in ["auth", "identity", "login", "trust"]):
        return "Core Identity"
    if any(k in name or k in desc for k in ["sync", "broker", "routing", "accessibility", "media"]):
        return "Accessibility Tools"
    if any(k in name or k in desc for k in ["magician", "agent", "founder", "business", "compliance"]):
        return "Business Magicians"
    if any(k in name or k in desc for k in ["mbtq", "testbed", "dev"]):
        return "Ecosystem Lab"

    return "Community Projects"

def collect_updates():
    updates = []
    seen = set()
    orgs = [s.strip() for s in ORG_LIST.split(",") if s.strip()]
    all_entities = [("user", MAIN_USER)] + [("org", org) for org in orgs]

    for entity_type, entity in all_entities:
        repos = get_repositories(entity, entity_type)
        if not repos:
            continue

        for repo in repos:
            full = repo["full_name"]
            if full in seen: continue
            seen.add(full)

            desc = repo.get("description") or ""
            # Exclude forked repos and incomplete repos
            if repo.get("fork") or not desc or desc.upper() == "NULL" or "(forked)" in desc.lower():
                continue

            status = classify_repo(repo, OFFICIAL_ORG)
            category = categorize_repo(repo)
            info = {
                "repo": repo["name"],
                "full_name": full,
                "url": repo['html_url'],
                "description": desc,
                "updated_at": repo.get("updated_at"),
                "open_issues": get_open_issues(repo["owner"]["login"], repo["name"]),
                "open_prs": get_open_pull_requests(repo["owner"]["login"], repo["name"]),
                "latest_commit": get_latest_commit(repo["owner"]["login"], repo["name"]),
                "latest_release": get_latest_release(repo["owner"]["login"], repo["name"]),
                "private": repo.get("private", False),
                "owner": repo["owner"]["login"],
                "org": entity if entity_type == "org" else None,
                "status": status,
                "category": category,
            }
            updates.append(info)

    # If no repos were found (e.g. rate limit), use fallback
    if not updates:
        print("No repositories fetched. Using fallback data.")
        return FALLBACK_REPOS

    return updates

def write_json(updates):
    os.makedirs("site", exist_ok=True)

    infra_status = {}
    if os.path.exists("infrastructure-status.json"):
        try:
            with open("infrastructure-status.json", "r") as f:
                infra_status = json.load(f)
        except Exception as e:
            print(f"Error reading infrastructure-status.json: {e}")

    output_data = {
        "updated": datetime.now(timezone.utc).isoformat(),
        "repos": updates,
        "infrastructure": infra_status
    }

    with open("site/updates.json", "w") as f:
        json.dump(output_data, f, indent=2)

def main():
    # Attempt to collect updates
    try:
        updates = collect_updates()
    except Exception as e:
        print(f"Error collecting updates from GitHub: {e}")
        updates = FALLBACK_REPOS

    write_json(updates)

    # Copy the high-fidelity UI template to the site directory
    if os.path.exists(".site/index.html"):
        shutil.copy(".site/index.html", "site/index.html")
    else:
        print("Warning: .site/index.html not found, skipping UI copy.")

if __name__ == "__main__":
    main()
