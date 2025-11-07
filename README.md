# Project Updates Aggregator

A GitHub Pages site that aggregates recent activity (releases, commits, open PRs/issues) across all repositories for your user **and** your selected organizations. Designed with accessibility (deaf-first, text-first) and org migration in mind, it highlights official organization repos and can support platform-wide consolidation.

---

## Features

- **Aggregates activity:** Gets latest release, latest commit, open issues & PRs for all user repos and any number of designated organizations.
- **Accessible:** Large text, clear headings, skip links, ARIA landmarks; all information readable without audio.
- **"Official" indicator:** Repos in your main organization are marked as "Official".
- **Supports future migration:** Easily adapt as projects move from your user account to your org or are mirrored.
- **JSON feed:** Static updates.json provides a live API feed for further use.

---

## Setup

1. **Repository:** Use a GitHub Pages repo, e.g. `pinkycollie/pinkycollie.github.io`.
2. **Add these secrets:**  
   - `PERSONAL_ACCESS_TOKEN` — Personal access token with `repo` and `read:org` scopes (so you see private and org repos).
   - `ORG_LIST` — Comma-separated list of orgs to aggregate (e.g. `officialorg,otherorg`).
   - `OFFICIAL_ORG` — Main org slug (e.g. `officialorg`).
3. **Enable GitHub Pages:** Serve from `gh-pages` branch (set by your repo → Settings → Pages).
4. **(Optional) Workflow customization:** Change schedule, add further fields and pages.

---

## How It Works

- Workflow runs daily and on push.
- `scripts/fetch_updates.py`:
    - Queries all repos for your user and orgs.
    - Builds per-repo update info (release, commit, open issues/PRs).
    - Tags repos as "official" (if in main org) or "fork" if they are forks.
    - Renders `site/index.html` and `site/updates.json`.
- `peaceiris/actions-gh-pages` deploys `site/` to your GitHub Pages branch.

---

## Accessibility Principles

- Text-first, large fonts, high contrast.
- Clear headings/landmarks for screen readers and navigation.
- Keyboard "skip to content" link.
- No audio-only content; space for transcripts/captions if multimedia added.

---

## Customization Ideas

- Add per-repo detail pages or filters.
- Generate RSS or Atom feeds.
- Add migration/mirroring status per repo.
- Integrate more badges: archived, fork, mirror, etc.
- Display PR/issue trends.
- Style with your org branding.

---

## Example Output

- Main `index.html`: List of updates for each repo
- Marked badges for official, fork, or personal repos
- JSON feed: `/updates.json`

---

## License

MIT License. 
&copy; pinkycollie and contributors.
