#!/bin/bash
set -e

echo "🏗️  Building all documentation sites..."

# 1. Get the absolute path of the project root
ROOT_DIR=$(pwd)

# 2. Clean previous builds
rm -rf "$ROOT_DIR/site"
mkdir -p "$ROOT_DIR/site"

# 3. Build landing page (to the root of /site)
echo "📄 Building landing page..."
cd "$ROOT_DIR/datatruck-docs/landing"
mkdocs build --clean -d "$ROOT_DIR/site"

# 4. Build DevOps docs (to /site/devops)
echo "⚙️  Building DevOps docs..."
cd "$ROOT_DIR/datatruck-docs/devops"
mkdocs build --clean -d "$ROOT_DIR/site/devops"

# 5. Build Backend docs (to /site/backend)
echo "💻 Building Backend docs..."
cd "$ROOT_DIR/datatruck-docs/backend"
mkdocs build --clean -d "$ROOT_DIR/site/backend"

# 6. Build AI docs (to /site/ai)
echo "🧠 Building AI docs..."
cd "$ROOT_DIR/datatruck-docs/ai"
mkdocs build --clean -d "$ROOT_DIR/site/ai"

# 7. Build Frontend docs (to /site/frontend)
echo "🎨 Building Frontend docs..."
cd "$ROOT_DIR/datatruck-docs/frontend"
mkdocs build --clean -d "$ROOT_DIR/site/frontend"

# 8. Return to root directory
cd "$ROOT_DIR"

echo "✅ All sites built successfully!"
echo "📦 Output directory: $ROOT_DIR/site/"