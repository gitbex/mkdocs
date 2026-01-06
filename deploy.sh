#!/bin/bash
set -e

echo "🏗️  Building all documentation sites..."

# Clean previous builds
rm -rf site/

# Build landing page (root)
echo "📄 Building landing page..."
cd datatruck-docs/landing
mkdocs build --clean -d ../site
cd ../..

# Build DevOps docs
echo "⚙️  Building DevOps docs..."
cd datatruck-docs/devops
mkdocs build --clean -d ../site/devops
cd ../..

# Build Backend docs
echo "💻 Building Backend docs..."
cd datatruck-docs/backend
mkdocs build --clean -d ../site/backend
cd ../..

# Build Frontend docs
echo "🎨 Building Frontend docs..."
cd datatruck-docs/frontend
mkdocs build --clean -d ../site/frontend
cd ../..

echo "✅ All sites built successfully!"
echo "📦 Output directory: ./site/"