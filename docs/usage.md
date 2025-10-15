# Usage Guide

Learn how to use SSVproff effectively for file management and automation.

## Basic Operations

### Uploading Files

#### Using DVC

```bash
# Add files to DVC tracking
dvc add data/large-file.bin

# Commit the .dvc file
git add data/large-file.bin.dvc data/.gitignore
git commit -m "Add large file"

# Push to remote storage
dvc push
```

#### Using rclone

```bash
# Upload a single file
rclone copy local-file.txt b2storage:bucket/path/

# Upload a directory
rclone sync local-dir/ b2storage:bucket/dir/

# Upload with progress
rclone copy local-file.txt b2storage:bucket/ --progress
```

### Downloading Files

#### Using DVC

```bash
# Pull tracked files
dvc pull

# Pull specific file
dvc pull data/large-file.bin.dvc
```

#### Using rclone

```bash
# Download a file
rclone copy b2storage:bucket/file.txt ./

# Download a directory
rclone sync b2storage:bucket/dir/ ./local-dir/
```

## File Management

### Listing Files

```bash
# List files in B2 bucket
rclone ls b2storage:bucket/

# List with details
rclone lsl b2storage:bucket/

# List directories only
rclone lsd b2storage:bucket/
```

### Deleting Files

```bash
# Delete a file
rclone delete b2storage:bucket/file.txt

# Delete a directory
rclone purge b2storage:bucket/old-dir/
```

## Automation

### Scheduled Sync

The repository includes automated sync workflows that run every 6 hours.

### Manual Triggers

Trigger workflows manually:

```bash
# Using GitHub CLI
gh workflow run sync.yml
```

## Version Control

### Tracking Changes

```bash
# Check DVC status
dvc status

# View file history
git log -- data/file.bin.dvc
```

### Reverting Changes

```bash
# Revert to previous version
git checkout HEAD~1 data/file.bin.dvc
dvc checkout
```

## Best Practices

### File Organization

```
data/
├── raw/          # Original, immutable data
├── processed/    # Cleaned and transformed data
├── models/       # Trained models
└── outputs/      # Analysis results
```

### Naming Conventions

- Use lowercase with hyphens: `my-file.txt`
- Include dates for versioned files: `report-2024-01-15.pdf`
- Use descriptive names: `customer-data-cleaned.csv`

## Next Steps

- [API Reference](api.md) - Detailed API documentation
- [Security Guide](security.md) - Security best practices
- [Configuration](configuration.md) - Advanced configuration options
