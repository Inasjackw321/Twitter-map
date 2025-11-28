# GitHub Pages Deployment

This folder contains the GitHub Pages website for the Twitter Conflict Map Generator.

## 🌐 Live Website

Once deployed, your website will be available at:
**https://Inasjackw321.github.io/Twitter-map/**

## 📁 Structure

```
docs/
├── index.html          # Main website page
├── maps/              # Generated map files (deployed here)
│   ├── ukraine_russia_map.html
│   ├── israel_iran_map.html
│   ├── china_taiwan_map.html
│   └── us_venezuela_map.html
└── README.md          # This file
```

## 🚀 How to Deploy

### Step 1: Generate Maps Locally

```bash
# Go to project root
cd ..

# Generate maps
python main.py ukraine_russia
python main.py israel_iran
python main.py china_taiwan
python main.py us_venezuela
```

### Step 2: Copy Maps to Docs Folder

```bash
# Run the deployment script
./deploy_to_pages.sh
```

This will copy all generated maps from `maps/` to `docs/maps/`.

### Step 3: Push to GitHub

```bash
git add docs/
git commit -m "Update GitHub Pages with new maps"
git push origin main
```

### Step 4: Enable GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings** → **Pages**
3. Under **Source**, select:
   - Branch: `main`
   - Folder: `/docs`
4. Click **Save**
5. Wait a few minutes for deployment

Your site will be live at: `https://Inasjackw321.github.io/Twitter-map/`

## 🔄 Updating Maps

To update with fresh data:

1. Run scripts locally to generate new maps
2. Run `./deploy_to_pages.sh`
3. Commit and push changes
4. GitHub Pages will auto-update in a few minutes

## 📝 Notes

- The website is static HTML/CSS/JavaScript
- No server-side code runs on GitHub Pages
- Maps must be generated locally using Python scripts
- Twitter API calls happen on your local machine only
