#!/bin/bash
# Script to reorganize monorepo structure to packages/* layout
# Usage: bash scripts/setup-packages.sh

set -e

echo "🔧 Setting up packages structure for SSVproff monorepo..."

# Create packages directories
mkdir -p packages/api packages/web

echo "✅ Created packages/api and packages/web directories"

# Optional: Move existing api and web if they exist at root
if [ -d "api" ] && [ ! -d "packages/api/src" ]; then
  echo "📦 Moving api/ to packages/api/..."
  cp -r api/* packages/api/ 2>/dev/null || true
fi

if [ -d "web" ] && [ ! -d "packages/web/src" ]; then
  echo "📦 Moving web/ to packages/web/..."
  cp -r web/* packages/web/ 2>/dev/null || true
fi

# Create workspace package.json if it doesn't exist
if [ ! -f "package.json" ]; then
  echo "📝 Creating root package.json with workspaces..."
  cat > package.json << 'EOF'
{
  "name": "ssvproff-monorepo",
  "version": "1.0.0",
  "private": true,
  "workspaces": [
    "packages/*"
  ],
  "scripts": {
    "dev:api": "cd packages/api && npm run dev",
    "dev:web": "cd packages/web && npm run dev",
    "build:api": "cd packages/api && npm run build",
    "build:web": "cd packages/web && npm run build",
    "test": "npm run test --workspaces",
    "lint": "npm run lint --workspaces"
  },
  "devDependencies": {
    "turbo": "^1.10.0"
  }
}
EOF
fi

# Create turbo.json for build optimization
if [ ! -f "turbo.json" ]; then
  echo "⚡ Creating turbo.json for optimized builds..."
  cat > turbo.json << 'EOF'
{
  "$schema": "https://turbo.build/schema.json",
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".next/**"]
    },
    "dev": {
      "cache": false,
      "persistent": true
    },
    "lint": {
      "outputs": []
    },
    "test": {
      "dependsOn": ["^build"],
      "outputs": ["coverage/**"]
    }
  }
}
EOF
fi

echo ""
echo "✨ Packages structure setup complete!"
echo ""
echo "📁 Structure:"
echo "   packages/"
echo "     ├── api/     - Backend API"
echo "     └── web/     - Frontend Web"
echo ""
echo "🚀 Next steps:"
echo "   1. npm install (install dependencies)"
echo "   2. npm run dev:api (start API server)"
echo "   3. npm run dev:web (start Web server)"
echo ""
echo "💡 Use 'turbo' for optimized builds:"
echo "   npx turbo run build"
echo ""
