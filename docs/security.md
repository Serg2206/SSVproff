# Security Guide

Best practices and security features for SSVproff.

## Overview

Security is a top priority in SSVproff. This guide covers authentication, encryption, access control, and best practices for keeping your data secure.

## Authentication & Authorization

### GitHub Authentication

#### Personal Access Tokens
- Use fine-grained tokens with minimal required scopes
- Rotate tokens regularly (every 90 days recommended)
- Never commit tokens to repository
- Store tokens in GitHub Secrets or environment variables

```bash
# Set token as environment variable
export GITHUB_TOKEN="your_token_here"

# Use in scripts
curl -H "Authorization: Bearer $GITHUB_TOKEN" \
  https://api.github.com/repos/Serg2206/SSVproff
```

#### Required Scopes
- `repo` - Repository access
- `workflow` - Workflow management
- `read:org` - Organization access (if applicable)

### Backblaze B2 Authentication

#### Application Keys
- Create separate keys for different purposes
- Use restricted keys with minimal permissions
- Enable key restrictions:
  - Bucket-specific access
  - Read-only when possible
  - IP restrictions if applicable

## Data Encryption

### Encryption at Rest

#### Backblaze B2
- Server-side encryption enabled by default
- Uses AES-256 encryption
- Encryption keys managed by Backblaze

#### Local Encryption
For sensitive files, encrypt before upload:

```bash
# Encrypt file with GPG
gpg --symmetric --cipher-algo AES256 sensitive-file.txt

# Upload encrypted file
rclone copy sensitive-file.txt.gpg b2storage:bucket/

# Decrypt after download
gpg --decrypt sensitive-file.txt.gpg > sensitive-file.txt
```

### Encryption in Transit

- All API calls use HTTPS/TLS 1.2+
- rclone uses encrypted connections by default
- GitHub Actions uses secure runners

## Access Control

### Repository Permissions

#### Branch Protection
Enable branch protection for main branch:

```yaml
branches:
  - name: main
    protection:
      required_pull_request_reviews:
        required_approving_review_count: 1
      required_status_checks:
        strict: true
      enforce_admins: true
```

### Secrets Management

#### GitHub Secrets
Store sensitive data in GitHub Secrets:

1. Go to repository Settings → Secrets and variables → Actions
2. Add new repository secret
3. Use in workflows:

```yaml
- name: Use secret
  env:
    API_KEY: ${{ secrets.API_KEY }}
  run: ./script.sh
```

## Security Best Practices

### 1. Principle of Least Privilege
- Grant minimum necessary permissions
- Use read-only access when possible
- Regularly audit access rights

### 2. Regular Updates
```bash
# Update dependencies
npm audit fix
pip install --upgrade -r requirements.txt
```

### 3. Input Validation
```typescript
function validatePath(path: string): boolean {
  // Prevent path traversal
  if (path.includes('..')) {
    throw new Error('Invalid path');
  }
  return true;
}
```

## Security Checklist

- [ ] All secrets stored in GitHub Secrets
- [ ] Branch protection enabled
- [ ] Required reviews configured
- [ ] Security scanning enabled
- [ ] Access regularly reviewed
- [ ] Tokens rotated regularly
- [ ] Encryption enabled
- [ ] Backups tested

## Next Steps

- [API Reference](api.md) - Secure API usage
- [Configuration](configuration.md) - Security settings
- [Usage Guide](usage.md) - Secure operations
