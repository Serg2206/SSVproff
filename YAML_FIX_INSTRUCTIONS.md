# GitHub Pages Workflow YAML Syntax Fix

## Issue Identified
The `.github/workflows/pages.yml` file has severe YAML syntax errors due to incorrect indentation throughout the file. The main issues are:

1. **Line 6**: `workflow_dispatch:` is incorrectly nested under `push:` instead of being at the same level under `on:`
2. **Lines 8-11**: `permissions:` block is incorrectly nested under `on:` instead of being at the root level
3. **Line 13**: `jobs:` is incorrectly nested instead of being at the root level
4. **Throughout**: Excessive and inconsistent indentation (hundreds of spaces instead of standard 2-space indentation)

## YAML Parser Error
```
yaml.parser.ParserError: while parsing a block mapping
  in ".github/workflows/pages.yml", line 5, column 7
expected <block end>, but found '<block mapping start>'
  in ".github/workflows/pages.yml", line 6, column 11
```

## Solution

### Why I Cannot Fix This Automatically
The Abacus.AI GitHub App currently lacks the `workflows` permission required to modify workflow files. This is a GitHub security restriction that prevents apps from modifying CI/CD workflows without explicit permission.

**Error received:**
```
refusing to allow a GitHub App to create or update workflow `.github/workflows/pages.yml` without `workflows` permission
```

### Manual Fix Required

You need to manually replace the content of `.github/workflows/pages.yml` with the corrected version below.

## Corrected YAML File

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Build MkDocs
        run: |
          cd docs
          pip install -r requirements.txt
          mkdocs build -d ../public/docs

      - name: Build Next.js
        run: |
          cd web
          npm ci
          npm run build
          mv out ../public/web

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./public

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

## How to Apply the Fix

### Option 1: Direct Edit on GitHub (Recommended)
1. Go to: https://github.com/Serg2206/SSVproff/edit/main/.github/workflows/pages.yml
2. Select all content (Ctrl+A / Cmd+A)
3. Delete it
4. Copy the corrected YAML from above
5. Paste it into the editor
6. Commit with message: "Fix YAML syntax errors in pages workflow"

### Option 2: Using Git Locally
```bash
cd /path/to/your/local/repo
git checkout main
git pull origin main

# Replace the file content with the corrected version
# (copy from the corrected YAML above)

git add .github/workflows/pages.yml
git commit -m "Fix YAML syntax errors in pages workflow"
git push origin main
```

## After Fixing

Once you've applied the fix:

1. **The workflow will automatically trigger** on the next push to main
2. **Check the Actions tab**: https://github.com/Serg2206/SSVproff/actions
3. **Monitor the workflow run** to ensure it completes successfully
4. **GitHub Pages will be deployed** to: https://serg2206.github.io/SSVproff/

## Verification Steps

After the workflow runs successfully:

1. Check Actions tab for green checkmark
2. Go to Settings → Pages to see the deployment status
3. Visit the GitHub Pages URL to see your deployed site

## Key Changes Made

- ✅ Fixed `on:` block structure (push and workflow_dispatch at same level)
- ✅ Moved `permissions:` to root level
- ✅ Moved `jobs:` to root level
- ✅ Standardized indentation to 2 spaces throughout
- ✅ Verified YAML syntax is valid using Python yaml parser

## GitHub Pages Configuration

After the workflow runs successfully, GitHub Pages should be automatically configured to deploy from GitHub Actions. If not, you may need to:

1. Go to: https://github.com/Serg2206/SSVproff/settings/pages
2. Under "Build and deployment"
3. Set Source to: "GitHub Actions"

---

**Note**: I've also saved the corrected file as `pages.yml.corrected` in this repository for your reference.
