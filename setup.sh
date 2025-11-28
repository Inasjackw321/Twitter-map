#!/bin/bash
# Setup script for Twitter Conflict Map Generator

echo "============================================"
echo "Twitter Conflict Map Generator - Setup"
echo "============================================"
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python $python_version"

# Install requirements
echo ""
echo "Installing Python dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "Error installing dependencies!"
    exit 1
fi

# Check if .env exists
echo ""
if [ -f .env ]; then
    echo "✓ .env file found"
else
    echo "⚠ .env file not found"
    echo ""
    echo "Creating .env from template..."
    cp .env.example .env
    echo ""
    echo "IMPORTANT: Please edit the .env file and add your Twitter API credentials!"
    echo ""
    echo "To get Twitter API credentials:"
    echo "1. Go to https://developer.twitter.com/en/portal/dashboard"
    echo "2. Create a new project and app"
    echo "3. Generate your Bearer Token"
    echo "4. Copy the credentials to your .env file"
    echo ""
fi

# Create directories
echo "Creating data and maps directories..."
mkdir -p data maps

echo ""
echo "============================================"
echo "Setup Complete!"
echo "============================================"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your Twitter API credentials (if not done yet)"
echo "2. Run: python main.py <region>"
echo "   where <region> is one of:"
echo "   - ukraine_russia"
echo "   - israel_iran"
echo "   - china_taiwan"
echo "   - us_venezuela"
echo ""
echo "Or run all regions at once with: ./run_all.sh"
echo ""
