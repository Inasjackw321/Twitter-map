#!/bin/bash
# Deploy generated maps to GitHub Pages (docs folder)

echo "============================================"
echo "Deploy to GitHub Pages"
echo "============================================"
echo ""

# Check if maps directory exists
if [ ! -d "maps" ]; then
    echo "❌ Error: No 'maps' directory found!"
    echo "Generate at least one map first:"
    echo "  python main.py ukraine_russia"
    exit 1
fi

# Check if any maps exist
map_count=$(find maps -name "*.html" 2>/dev/null | wc -l)
if [ "$map_count" -eq 0 ]; then
    echo "❌ Error: No map files found in 'maps' directory!"
    echo "Generate at least one map first:"
    echo "  python main.py ukraine_russia"
    exit 1
fi

echo "Found $map_count map file(s) to deploy"
echo ""

# Create docs/maps directory if it doesn't exist
mkdir -p docs/maps

# Copy all HTML maps to docs/maps
echo "📋 Copying map files..."
cp -v maps/*.html docs/maps/ 2>/dev/null

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Maps copied successfully!"
else
    echo ""
    echo "⚠️  Warning: No maps were copied"
fi

# List deployed maps
echo ""
echo "============================================"
echo "Deployed Maps:"
echo "============================================"
ls -lh docs/maps/*.html 2>/dev/null || echo "No maps found"

echo ""
echo "============================================"
echo "Next Steps:"
echo "============================================"
echo ""
echo "1. Commit and push the changes:"
echo "   git add docs/"
echo "   git commit -m 'Update GitHub Pages with new maps'"
echo "   git push origin main"
echo ""
echo "2. Enable GitHub Pages (if not already enabled):"
echo "   - Go to your repository on GitHub"
echo "   - Settings → Pages"
echo "   - Source: Deploy from branch"
echo "   - Branch: main → /docs"
echo "   - Click Save"
echo ""
echo "3. Your site will be available at:"
echo "   https://Inasjackw321.github.io/Twitter-map/"
echo ""
echo "============================================"
