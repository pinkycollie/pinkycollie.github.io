[![Infrastructure Gate](https://github.com/pinkycollie/pinkycollie.github.io/actions/workflows/infrastructure-gate.yml/badge.svg)](https://github.com/pinkycollie/pinkycollie.github.io/actions/workflows/infrastructure-gate.yml)

# Pinky Collie — Personal Site

A GitHub Pages site showcasing Pinky Collie's work as a Deaf-first business architect and systems builder. This site highlights platforms, expertise, and accessibility-first approach to building technology for the Deaf community.

---

## About

<div align="center">

# 👋 Hi, I'm @pinkycollie

### **Deaf System Architect** • **Accessibility & Ecosystem Builder** • **Pmaster-dev**

[![Deaf-First Engineering](https://img.shields.io/badge/DeafAUTH-Identity_Backbone-ff0974?style=for-the-badge&logo=github)](https://github.com/pinkycollie)
[![Accessibility Focus](https://img.shields.io/badge/WCAG-2.1_AAA-purple?style=for-the-badge)](https://github.com/pinkycollie)
[![Platform](https://img.shields.io/badge/EcoSystem-PinkSync_%7C_Fibonrose_%7C_VR4Deaf-00d2ff?style=for-the-badge)](https://github.com/Pmaster-dev)

---

> *"Architecting accessible, sustainable systems built to outlast decades — empowering entrepreneurs with disabilities through zero-friction automation."*

</div>

---

### ⚡ Architectural DNA

* 🛠️ **Identity & Security:** Standardizing authentication via **DeafAUTH** (Supabase OAuth Server / Google IdP integration).
* 🛰️ **Core Ecosystem:** Building **PinkSync** & **Fibonrose** trust engines for automated workflow execution.
* ♿ **VR4Deaf & Disability Enterprise:** Crafting milestone-based startup pipelines for VR (Vocational Rehabilitation) partners, business specialists, and clients.
* ⏳ **Long-Term Mission:** Designing 25+ year resilient infrastructure combining low-code ease (AppSheet / Google Workspace) with sovereign high-performance backends (Node, Python, Supabase, Vercel, GCP).

---

### 💻 Stack & Ecosystem Matrix

| Layer | Technologies & Tools |
| :--- | :--- |
| **Auth & Identity** | `DeafAUTH`, `Supabase OAuth`, `Google IdP` |
| **Core Systems** | `PinkSync`, `Fibonrose`, `Node.js`, `Python` |
| **AI & Automation** | `Gemini`, `Google AI Studio`, `Google Apps Script` |
| **Cloud & Deployment** | `Vercel`, `Google Cloud Platform (GCP)`, `Firebase` |
| **Frontends & Forms** | `AppSheet`, `Google Workspace`, `React / Next.js` |
| **Standards** | `WCAG 2.1 AAA Compliance`, `Data Isolation Schemas` |

---

### 📊 System Architecture Snapshot

```mermaid
flowchart LR
    A[VR Partner / Google Form] --> B[AppSheet & Apps Script Orchestrator]
    B --> C[Supabase & DeafAUTH]
    C --> D[PinkSync / Fibonrose Workflows]
    D --> E[Gemini AI Automation]
    E --> F[Client & Specialist Dashboard]


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
