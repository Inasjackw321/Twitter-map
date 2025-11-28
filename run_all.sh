#!/bin/bash
# Quick script to generate maps for all 4 regions

echo "============================================"
echo "Twitter Conflict Map Generator - Run All"
echo "============================================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "Error: .env file not found!"
    echo "Please create a .env file with your Twitter API credentials."
    echo "See .env.example for the required format."
    exit 1
fi

# Array of regions
regions=("ukraine_russia" "israel_iran" "china_taiwan" "us_venezuela")

# Loop through each region
for region in "${regions[@]}"
do
    echo ""
    echo "============================================"
    echo "Processing: $region"
    echo "============================================"
    python main.py "$region" --max-tweets 100

    if [ $? -ne 0 ]; then
        echo "Error processing $region"
        read -p "Continue with next region? (y/n) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi

    echo ""
    echo "Waiting 5 seconds before next region (rate limiting)..."
    sleep 5
done

echo ""
echo "============================================"
echo "All maps generated successfully!"
echo "============================================"
echo ""
echo "Maps are saved in the 'maps/' directory:"
ls -lh maps/*.html

echo ""
echo "Open any map file in your browser to view results."
