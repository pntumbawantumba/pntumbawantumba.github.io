#!/bin/bash

# Exit on error
set -e

echo "🚀 Rebuilding Hugo site..."
hugo


if [ -d "docs" ]; then
    echo "🗑 Cleaning docs folder..."
    rm -rf docs/*
else
    echo "📁 docs folder does not exist. Creating..."
    mkdir docs
fi

echo "📦 Copying public files to docs..."
cp -r public/* docs/

echo "💾 Adding changes to git..."
git add docs

echo "📝 Committing changes..."
git commit -m "Update site"

echo "📤 Pushing to remote..."
git push

echo "✅ Deployment complete!"