#!/bin/bash
set -e

echo "🏗️  Building all documentation sites..."

# Clean previous builds
rm -rf site/

# Build landing page (root)
echo "📄 Building landing page..."
cd landing
mkdocs build --clean -d ../site
cd ..

# Build DevOps docs
echo "⚙️  Building DevOps docs..."
cd devops
mkdocs build --clean -d ../site/devops
cd ..

# Build Backend docs
echo "💻 Building Backend docs..."
cd backend
mkdocs build --clean -d ../site/backend
cd ..

# Build Frontend docs
echo "🎨 Building Frontend docs..."
cd frontend
mkdocs build --clean -d ../site/frontend
cd ..

# Build AI docs
echo "🤖 Building AI docs..."
cd ai
mkdocs build --clean -d ../site/ai
cd ..

echo "✅ All sites built successfully!"
echo "📦 Output directory: ./site/"