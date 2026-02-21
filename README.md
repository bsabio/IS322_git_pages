# 🤖 AI Consultant — GitHub Pages Starter

A **one-click, forkable** website for AI consultants.  
Edit a single JSON file in your browser → GitHub Actions builds and deploys your site automatically. No local software needed.

---

## 🚀 Quick Start (5 minutes)

### 1. Fork this Repository

Click the **Fork** button at the top-right of this page.  
This creates your own copy under `https://github.com/<YOUR_USERNAME>/IS322_git_pages`.

### 2. Enable GitHub Actions Permissions

> **This step is required** or the automated deploy will fail.

1. Go to **Settings → Actions → General** in your forked repo.
2. Under **Workflow permissions**, select **Read and write permissions**.
3. Click **Save**.

### 3. Enable GitHub Pages

1. Go to **Settings → Pages**.
2. Under **Source**, select the branch **gh-pages** and folder **/ (root)**.
3. Click **Save**.

> ⏳ The `gh-pages` branch is created automatically after your first push. If you don't see it yet, make an edit (Step 4) and come back here.

### 4. Customize Your Site

1. Open `content.json` in your forked repo (click the file, then the ✏️ pencil icon).
2. Replace the placeholder text with your own info:
   - **name** — Your full name
   - **title** — Your professional title
   - **bio** — A short paragraph about you
   - **services** — Update titles, descriptions, and emoji icons
   - **contact** — Your email, LinkedIn, GitHub, and location
3. Commit the change (green **Commit changes** button).

That's it! GitHub Actions will automatically rebuild and deploy your site within ~60 seconds.

### 5. View Your Live Site

Your site will be live at:

```
https://<YOUR_USERNAME>.github.io/IS322_git_pages/
```

---

## 📁 Project Structure

| File | Purpose |
|------|---------|
| `content.json` | **Your site data** — the only file you need to edit |
| `template.html` | HTML/CSS template (Tailwind CSS via CDN) |
| `build_site.py` | Python script that combines JSON + template → `index.html` |
| `.github/workflows/deploy.yml` | GitHub Actions workflow (build + deploy) |

---

## 🛠 How It Works

```
content.json  ─┐
                ├──▶  build_site.py  ──▶  index.html  ──▶  GitHub Pages (gh-pages branch)
template.html ─┘
```

1. You edit `content.json` in your browser and commit.
2. GitHub Actions detects the push to `main`.
3. The workflow runs `build_site.py` to generate `index.html`.
4. The generated file is deployed to the `gh-pages` branch.
5. GitHub Pages serves your live site.

---

## ❓ Troubleshooting

| Problem | Fix |
|---------|-----|
| Actions tab shows a failed workflow | Go to **Settings → Actions → General** and enable **Read and write permissions** |
| Site not loading after deploy | Go to **Settings → Pages** and make sure **Source** is set to `gh-pages` / `/ (root)` |
| Changes not appearing | Wait ~60 seconds, then hard-refresh your browser (`Ctrl+Shift+R`) |

---

## 📝 License

MIT — feel free to use, modify, and share.