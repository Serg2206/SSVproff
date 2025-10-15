# API Reference

Complete API documentation for SSVproff.

## Overview

SSVproff provides a RESTful API for programmatic access to file management, storage operations, and automation features.

## Authentication

All API requests require authentication using a GitHub Personal Access Token.

### Getting a Token

1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate a new token with appropriate scopes:
   - `repo` - Full repository access
   - `workflow` - Workflow access

### Using the Token

Include the token in the Authorization header:

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.github.com/repos/Serg2206/SSVproff
```

## Endpoints

### Repository Information

#### Get Repository
```http
GET /repos/Serg2206/SSVproff
```

**Response:**
```json
{
  "id": 1077060956,
  "name": "SSVproff",
  "full_name": "Serg2206/SSVproff",
  "private": false,
  "description": "Repository description",
  "default_branch": "main"
}
```

### File Operations

#### Get File Content
```http
GET /repos/Serg2206/SSVproff/contents/{path}
```

**Parameters:**
- `path` (string): File path in repository
- `ref` (string, optional): Branch or commit SHA

**Response:**
```json
{
  "name": "file.txt",
  "path": "data/file.txt",
  "sha": "abc123...",
  "size": 1024,
  "content": "base64_encoded_content",
  "encoding": "base64"
}
```

## Code Examples

### TypeScript/JavaScript

```typescript
import { Octokit } from '@octokit/rest';

const octokit = new Octokit({
  auth: process.env.GITHUB_TOKEN
});

// Get file content
async function getFile(path: string) {
  const { data } = await octokit.repos.getContent({
    owner: 'Serg2206',
    repo: 'SSVproff',
    path: path
  });
  
  if ('content' in data) {
    const content = Buffer.from(data.content, 'base64').toString();
    return content;
  }
}
```

### Python

```python
import requests
import base64

class SSVproffAPI:
    def __init__(self, token):
        self.token = token
        self.base_url = 'https://api.github.com'
        self.headers = {
            'Authorization': f'Bearer {token}',
            'Accept': 'application/vnd.github.v3+json'
        }
    
    def get_file(self, path):
        url = f'{self.base_url}/repos/Serg2206/SSVproff/contents/{path}'
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        
        data = response.json()
        content = base64.b64decode(data['content']).decode()
        return content
```

## Rate Limits

GitHub API has rate limits:
- **Authenticated requests**: 5,000 per hour
- **Unauthenticated requests**: 60 per hour

## Error Handling

### Common Error Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 500 | Internal Server Error |

## Next Steps

- [Usage Guide](usage.md) - Practical examples
- [Security](security.md) - API security best practices
- [Configuration](configuration.md) - Advanced settings
