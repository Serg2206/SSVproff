# File Management

Comprehensive guide to managing files in SSVproff.

## File Structure

### Recommended Organization

```
SSVproff/
├── data/
│   ├── raw/              # Original data files
│   ├── processed/        # Processed data
│   ├── models/           # ML models
│   └── outputs/          # Results and reports
├── scripts/              # Automation scripts
├── docs/                 # Documentation
└── .github/workflows/    # CI/CD workflows
```

## File Operations

### Adding Files

#### Small Files (< 10MB)
Use Git directly:
```bash
git add file.txt
git commit -m "Add file"
git push
```

#### Large Files (> 10MB)
Use DVC:
```bash
dvc add data/large-file.bin
git add data/large-file.bin.dvc data/.gitignore
git commit -m "Add large file"
git push
dvc push
```

### Updating Files

```bash
# Modify the file
echo "new content" >> file.txt

# Track changes
dvc add data/file.bin
git add data/file.bin.dvc
git commit -m "Update file"
git push
dvc push
```

## Storage Management

### Checking Storage Usage

```bash
# Check local cache size
du -sh .dvc/cache

# Check remote storage
rclone size b2storage:bucket
```

### Cleaning Up

```bash
# Remove unused cache
dvc gc

# Clean old versions
dvc gc --workspace --cloud
```

## Next Steps

- [Automation Guide](automation.md) - Automate file operations
- [API Reference](api.md) - Programmatic file access
- [Security](security.md) - Secure file handling
