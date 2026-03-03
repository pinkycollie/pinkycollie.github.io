import fetch from "node-fetch";
import { writeFileSync } from "fs";

const OWNER = "pinkycollie";
const TOKEN = process.env.GITHUB_TOKEN; // set in repo secrets

async function fetchAllRepos() {
  let page = 1;
  const perPage = 100;
  const repos = [];

  while (true) {
    const res = await fetch(
      `https://api.github.com/users/${OWNER}/repos?per_page=${perPage}&page=${page}`,
      {
        headers: {
          "Accept": "application/vnd.github+json",
          ...(TOKEN ? { Authorization: `Bearer ${TOKEN}` } : {})
        }
      }
    );

    if (!res.ok) {
      console.error("GitHub API error:", res.status, await res.text());
      process.exit(1);
    }

    const data = await res.json();
    if (data.length === 0) break;

    repos.push(
      ...data.map(r => ({
        name: r.name,
        full_name: r.full_name,
        html_url: r.html_url,
        description: r.description,
        archived: r.archived,
        private: r.private,
        pushed_at: r.pushed_at,
        has_issues: r.has_issues,
        has_pages: r.has_pages,
        language: r.language
      }))
    );

    page++;
  }

  const payload = {
    owner: OWNER,
    lastUpdated: new Date().toISOString(),
    repos
  };

  writeFileSync("inventory/repos.json", JSON.stringify(payload, null, 2));
  console.log(`Saved ${repos.length} repos to inventory/repos.json`);
}

fetchAllRepos().catch(err => {
  console.error(err);
  process.exit(1);
});
