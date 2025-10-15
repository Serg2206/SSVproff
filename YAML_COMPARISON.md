# YAML Syntax Error Comparison

## Before (Broken - with syntax errors)

```yaml
name: Deploy to GitHub Pages

on:
    push:
      branches: [main]
          workflow_dispatch:    # ❌ WRONG: Should be at same level as 'push'

        permissions:            # ❌ WRONG: Should be at root level, not under 'on'
          contents: read
            pages: write        # ❌ WRONG: Excessive indentation
              id-token: write   # ❌ WRONG: Excessive indentation

              jobs:             # ❌ WRONG: Should be at root level
                build:
                    runs-on: ubuntu-latest
                        steps:  # ❌ WRONG: Excessive indentation continues...
```

## After (Fixed - valid YAML)

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:            # ✅ CORRECT: Same level as 'push'

permissions:                    # ✅ CORRECT: At root level
  contents: read
  pages: write                  # ✅ CORRECT: Proper 2-space indentation
  id-token: write               # ✅ CORRECT: Proper 2-space indentation

jobs:                           # ✅ CORRECT: At root level
  build:
    runs-on: ubuntu-latest
    steps:                      # ✅ CORRECT: Proper indentation
      - uses: actions/checkout@v4
```

## Key Differences

| Aspect | Before | After |
|--------|--------|-------|
| `workflow_dispatch` position | Nested under `push` | Same level as `push` under `on` |
| `permissions` position | Nested under `on` | Root level |
| `jobs` position | Nested under `permissions` | Root level |
| Indentation | Hundreds of spaces | Standard 2 spaces |
| YAML validity | ❌ Invalid | ✅ Valid |

## Structure Overview

### Correct YAML Structure
```
root
├── name
├── on
│   ├── push
│   └── workflow_dispatch
├── permissions
│   ├── contents
│   ├── pages
│   └── id-token
└── jobs
    ├── build
    │   ├── runs-on
    │   └── steps
    └── deploy
        ├── needs
        ├── runs-on
        ├── environment
        └── steps
```
