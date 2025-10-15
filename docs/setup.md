# Setup Guide

This guide will help you set up SSVproff on your system.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Git**: Version control system
- **Python 3.8+**: For DVC and automation scripts
- **Node.js 18+**: For TypeScript development
- **rclone**: For file synchronization

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/Serg2206/SSVproff.git
cd SSVproff
```

### 2. Install Dependencies

#### Python Dependencies
```bash
pip install -r requirements.txt
```

#### Node.js Dependencies
```bash
npm install
```

### 3. Configure Backblaze B2

1. Create a Backblaze B2 account at [backblaze.com](https://www.backblaze.com/b2/cloud-storage.html)
2. Create a new bucket for your storage
3. Generate application keys with appropriate permissions
4. Note your Key ID and Application Key

### 4. Configure rclone

Create an rclone configuration for Backblaze B2:

```bash
rclone config
```

Follow the prompts:
- Choose "n" for new remote
- Name: `b2storage`
- Storage type: `b2`
- Enter your Key ID and Application Key
- Accept defaults for other options

### 5. Initialize DVC

```bash
dvc init
dvc remote add -d storage b2://your-bucket-name
dvc remote modify storage account <your-key-id>
dvc remote modify storage key <your-application-key>
```

### 6. Configure GitHub Secrets

Add the following secrets to your GitHub repository:

- `B2_KEY_ID`: Your Backblaze B2 Key ID
- `B2_APPLICATION_KEY`: Your Backblaze B2 Application Key
- `RCLONE_CONFIG`: Your rclone configuration (base64 encoded)

To encode your rclone config:
```bash
cat ~/.config/rclone/rclone.conf | base64
```

## Verification

Verify your setup:

```bash
# Test rclone connection
rclone lsd b2storage:

# Test DVC
dvc status

# Run tests
npm test
```

## Next Steps

- [Configuration Guide](configuration.md) - Configure advanced settings
- [Usage Guide](usage.md) - Learn how to use SSVproff
- [API Reference](api.md) - Explore the API

## Troubleshooting

### rclone Connection Issues
- Verify your Key ID and Application Key
- Check your internet connection
- Ensure your bucket name is correct

### DVC Issues
- Make sure DVC is properly initialized
- Verify remote storage configuration
- Check file permissions

### GitHub Actions Failures
- Verify all secrets are correctly set
- Check workflow logs for specific errors
- Ensure repository permissions are correct

For more help, check the [Usage Guide](usage.md) or contact support.
