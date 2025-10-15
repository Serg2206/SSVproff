# Automation Guide

Automate your workflows with SSVproff's powerful automation features.

## GitHub Actions Workflows

### Available Workflows

#### 1. Sync Workflow
Automatically syncs files to Backblaze B2:

```yaml
name: Sync to B2
on:
  schedule:
    - cron: '0 */6 * * *'
  workflow_dispatch:

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup rclone
        run: curl https://rclone.org/install.sh | sudo bash
      - name: Sync files
        run: rclone sync ./data b2storage:bucket/data
```

#### 2. Pages Workflow
Builds and deploys documentation:

```yaml
name: Deploy Pages
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v4
      - name: Install dependencies
        run: pip install -r docs/requirements.txt
      - name: Build docs
        run: mkdocs build
      - name: Deploy
        uses: actions/deploy-pages@v4
```

## Scheduled Tasks

### Cron Syntax

```
┌───────────── minute (0 - 59)
│ ┌───────────── hour (0 - 23)
│ │ ┌───────────── day of month (1 - 31)
│ │ │ ┌───────────── month (1 - 12)
│ │ │ │ ┌───────────── day of week (0 - 6)
│ │ │ │ │
* * * * *
```

### Common Schedules

```yaml
# Every hour
- cron: '0 * * * *'

# Every 6 hours
- cron: '0 */6 * * *'

# Daily at midnight
- cron: '0 0 * * *'
```

## Best Practices

### Error Handling

```yaml
- name: Sync with retry
  run: |
    for i in {1..3}; do
      rclone sync ./data b2storage:bucket/data && break
      echo "Retry $i failed, waiting..."
      sleep 60
    done
```

## Next Steps

- [API Reference](api.md) - Programmatic automation
- [Security](security.md) - Secure automation practices
- [Configuration](configuration.md) - Advanced settings
