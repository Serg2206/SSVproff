# Configuration Guide

Learn how to configure SSVproff for your specific needs.

## Configuration Files

SSVproff uses several configuration files:

- `.dvc/config` - DVC configuration
- `rclone.conf` - rclone configuration
- `.github/workflows/` - GitHub Actions workflows
- `package.json` - Node.js project configuration

## Storage Configuration

### Backblaze B2 Settings

Edit `.dvc/config` to configure your B2 storage:

```ini
[core]
    remote = storage
['remote "storage"']
    url = b2://your-bucket-name
    account = your-key-id
    key = your-application-key
```

### rclone Configuration

Your `rclone.conf` should contain:

```ini
[b2storage]
type = b2
account = your-key-id
key = your-application-key
hard_delete = false
```

## Sync Settings

### Automatic Sync Schedule

Configure sync frequency in `.github/workflows/sync.yml`:

```yaml
on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours
```

### Sync Filters

Create `.rclone-filter` to exclude files:

```
- .git/
- node_modules/
- *.tmp
- .DS_Store
```

## Automation Configuration

### GitHub Actions Workflows

#### Sync Workflow
Located at `.github/workflows/sync.yml`:
- Runs on schedule or manual trigger
- Syncs files to B2 storage
- Updates DVC tracking

#### Pages Workflow
Located at `.github/workflows/pages.yml`:
- Builds and deploys documentation
- Runs on push to main branch

### Environment Variables

Set these in GitHub repository settings:

| Variable | Description | Required |
|----------|-------------|----------|
| `B2_KEY_ID` | Backblaze B2 Key ID | Yes |
| `B2_APPLICATION_KEY` | B2 Application Key | Yes |
| `RCLONE_CONFIG` | Base64 encoded rclone config | Yes |

## Security Configuration

### Access Control

Configure access levels:

```yaml
# .github/workflows/permissions.yml
permissions:
  contents: read
  pages: write
  id-token: write
```

### Encryption

Enable encryption for sensitive files:

```bash
dvc config cache.type symlink
dvc config cache.protected true
```

## Advanced Settings

### Performance Tuning

Optimize rclone performance:

```bash
rclone sync source: dest: \
  --transfers 8 \
  --checkers 16 \
  --buffer-size 256M
```

### Logging

Configure logging levels:

```bash
# Set DVC verbosity
dvc config core.verbosity 1

# Set rclone log level
rclone --log-level INFO
```

## Next Steps

- [Usage Guide](usage.md) - Learn how to use configured features
- [API Reference](api.md) - Explore API endpoints
- [Security](security.md) - Security best practices
