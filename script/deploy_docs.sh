#!/bin/bash

# Exit on error
set -e

echo "🚀 Rebuilding Hugo site..."
hugo

echo "🔀 Switching to gh-pages branch..."
git checkout gh-pages

echo "📦 Copying public files to docs..."
cp -r public/* docs/

echo "💾 Adding changes to git..."
git add docs

echo "📝 Committing changes..."
git commit -m "Update site"

echo "📤 Pushing to remote..."
git push

echo "✅ Deployment complete!"