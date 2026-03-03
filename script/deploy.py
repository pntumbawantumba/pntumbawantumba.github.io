#!/bin/bash
set -e

echo "📦 Building Hugo site..."
hugo

echo "🔀 Switching to gh-pages branch..."
git checkout gh-pages


echo "📂 Copying new site..."
cp -r public/* .

echo "📝 Committing changes..."
git add .
git commit -m "Update site $(date +'%Y-%m-%d %H:%M:%S')" || echo "No changes to commit."

echo "🚀 Pushing to gh-pages..."
git push origin gh-pages

echo "🔙 Returning to main branch..."
git checkout main

echo "✅ Deployment complete!"