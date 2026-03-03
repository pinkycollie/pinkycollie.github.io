import { readFileSync, writeFileSync } from "fs";

const inventory = JSON.parse(
  readFileSync("inventory/repos.json", "utf8")
);

function isActive(repo) {
  if (!repo.pushed_at) return false;
  const lastPush = new Date(repo.pushed_at);
  const days = (Date.now() - lastPush.getTime()) / (1000 * 60 * 60 * 24);
  return days <= 90; // active if updated in last 90 days
}

const active = [];
const inactive = [];

for (const r of inventory.repos) {
  (isActive(r) && !r.archived ? active : inactive).push(r);
}

function tableFor(list) {
  if (list.length === 0) return "_None_\n";

  let md = "| Repo | Status | Last Push | Pages | Issues | Lang |\n";
  md += "|------|--------|-----------|-------|--------|------|\n";
  for (const r of list) {
    md += `| [${r.name}](${r.html_url}) | ${r.archived ? "Archived" : "Active"} | ${r.pushed_at ?? "—"} | ${r.has_pages ? "✅" : "❌"} | ${r.has_issues ? "✅" : "❌"} | ${r.language ?? "—"} |\n`;
  }
  return md + "\n";
}

let out = `# Pinky Collie GitHub Overview

Owner: **${inventory.owner}**  
Last scan: **${inventory.lastUpdated ?? "unknown"}**

---

## Active repositories (recently updated, not archived)

${tableFor(active)}

---

## Inactive or archived repositories

${tableFor(inactive)}
`;

writeFileSync("dashboards/REPOS_DASHBOARD.md", out);
console.log("Updated dashboards/REPOS_DASHBOARD.md");
