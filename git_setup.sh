#!/bin/bash
# Run this script to initialize Git and push to GitHub
# Usage: bash git_setup.sh

echo "Initializing Git repository..."
git init
git add .
git commit -m "Initial commit: Little Lemon restaurant capstone project"

echo ""
echo "Now create a repo on GitHub, then run:"
echo "  git remote add origin https://github.com/YOUR_USERNAME/littlelemon.git"
echo "  git branch -M main"
echo "  git push -u origin main"
