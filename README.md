# Pinky Collie — Personal Site

A GitHub Pages site showcasing Pinky Collie's work as a Deaf-first business architect and systems builder. This site highlights platforms, expertise, and accessibility-first approach to building technology for the Deaf community.

---

## About

This is the personal website for **Pinky Collie**, featuring:

- **Deaf-First Architecture:** Building platforms like DeafAUTH, PinkSync, and 360Magicians
- **Business & Tech Integration:** Combining insurance, tax, real estate, and compliance expertise with modern cloud and AI technologies
- **Accessibility Focus:** Dark-mode design with high contrast, clear typography, and text-first approach
- **Modern Stack:** Supabase, TypeScript, Python, Cloud Run, Next.js, and AI copilots

---

## Site Structure

The site is built with:
- **Static HTML/CSS:** Pure HTML with embedded CSS, no build tools required
- **Modern Design:** Dark theme with gradient accents, responsive layout
- **Accessibility:** Space Grotesk font, high contrast, semantic HTML

---

## Deployment

The site is automatically deployed to GitHub Pages via GitHub Actions:
- The `site/` directory contains the static HTML page
- On push to `main` branch, the workflow deploys the site
- GitHub Pages serves the content from the `gh-pages` branch

### GitHub Actions Workflow Configuration

The deployment workflow (`.github/workflows/deploy.yml`) includes:

```yaml
jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Setup Pages
        uses: actions/configure-pages@v4
      
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: './site'
      
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

**Important:** The `environment` section is required for GitHub Pages deployment. Without it, the workflow will fail with an error about missing environment configuration.

---

## Accessibility Features

- **Deaf-First Design:** All content is visual and text-based
- **High Contrast:** Dark background with light text for readability
- **Clear Typography:** Space Grotesk font with appropriate sizing
- **Semantic HTML:** Proper heading structure and landmarks
- **Responsive:** Works on desktop and mobile devices

---

## License

MIT License. 
&copy; pinkycollie and contributors.
