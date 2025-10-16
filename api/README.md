# SSVproff API

FastAPI-based REST API with PostgreSQL database and JWT authentication.

## Features

- ✅ **FastAPI Framework**: Modern, fast Python web framework
- ✅ **PostgreSQL Database**: Robust relational database with SQLAlchemy ORM
- ✅ **JWT Authentication**: Secure token-based authentication
- ✅ **Password Hashing**: Bcrypt password encryption
- ✅ **Database Migrations**: Alembic for version-controlled schema changes
- ✅ **Comprehensive Tests**: Unit and integration tests with pytest
- ✅ **API Documentation**: Auto-generated OpenAPI (Swagger) documentation
- ✅ **Type Safety**: Full type hints with mypy support
- ✅ **Code Quality**: Linting with ruff and formatting with black

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 12+
- pip or poetry

### Installation

1. **Install dependencies:**
   ```bash
   cd api
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # For development
   ```

2. **Set up PostgreSQL database:**
   ```bash
   # Access PostgreSQL
   sudo -u postgres psql
   
   # Create database and user
   CREATE DATABASE ssvproff_db;
   CREATE USER ssvproff_user WITH PASSWORD 'ssvproff_password';
   GRANT ALL PRIVILEGES ON DATABASE ssvproff_db TO ssvproff_user;
   \q
   ```

3. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Run database migrations:**
   ```bash
   alembic upgrade head
   ```

5. **Start the development server:**
   ```bash
   uvicorn app.main:app --reload
   ```

6. **Access the API:**
   - API: http://localhost:8000
   - Interactive docs (Swagger UI): http://localhost:8000/docs
   - Alternative docs (ReDoc): http://localhost:8000/redoc

## Project Structure

```
api/
├── alembic/                    # Database migrations
│   ├── versions/              # Migration files
│   └── env.py                 # Alembic configuration
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── endpoints/    # API endpoint routes
│   │   │   └── api.py        # API router aggregator
│   │   └── deps.py           # Dependencies (auth, db)
│   ├── core/
│   │   ├── config.py         # Application settings
│   │   └── security.py       # Security utilities (JWT, passwords)
│   ├── db/
│   │   ├── base.py           # SQLAlchemy base
│   │   └── session.py        # Database session management
│   ├── models/
│   │   └── user.py           # User model
│   ├── schemas/
│   │   ├── user.py           # User Pydantic schemas
│   │   └── auth.py           # Auth Pydantic schemas
│   ├── services/
│   │   └── auth.py           # Authentication business logic
│   └── main.py               # FastAPI application
├── docs/
│   ├── authentication.md     # Authentication API documentation
│   └── database_setup.md     # Database setup guide
├── tests/
│   ├── test_auth_endpoints.py    # Auth endpoint tests
│   ├── test_database.py          # Database tests
│   ├── test_security.py          # Security utilities tests
│   └── conftest.py               # Pytest fixtures
├── .env.example              # Environment variables template
├── alembic.ini              # Alembic configuration
├── requirements.txt         # Production dependencies
└── requirements-dev.txt     # Development dependencies
```

## API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/v1/auth/register` | Register new user | No |
| POST | `/api/v1/auth/login` | Login and get tokens | No |
| GET | `/api/v1/auth/me` | Get current user | Yes |
| POST | `/api/v1/auth/refresh` | Refresh access token | No |

### Health Check

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/v1/health` | API health status | No |
| GET | `/health` | Legacy health check | No |

For detailed API documentation, see [Authentication Documentation](docs/authentication.md).

## Configuration

Key environment variables in `.env`:

```env
# API Configuration
PROJECT_NAME=SSVproff API
VERSION=0.1.0
API_V1_PREFIX=/api/v1
DEBUG=true

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000", "http://localhost:8000"]

# Security
SECRET_KEY=your-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database
DATABASE_URL=postgresql://ssvproff_user:ssvproff_password@localhost:5432/ssvproff_db

# Logging
LOG_LEVEL=INFO
```

**Generate a secure secret key:**
```bash
openssl rand -hex 32
```

## Database Management

### Migrations

```bash
# Create a new migration
alembic revision -m "Description"

# Apply migrations
alembic upgrade head

# Rollback one revision
alembic downgrade -1

# View migration history
alembic history

# Check current revision
alembic current
```

For detailed database setup, see [Database Setup Guide](docs/database_setup.md).

## Testing

### Run all tests:
```bash
pytest
```

### Run with coverage:
```bash
pytest --cov=app --cov-report=html
```

### Run specific test file:
```bash
pytest tests/test_auth_endpoints.py
```

### Run specific test:
```bash
pytest tests/test_auth_endpoints.py::TestLoginEndpoint::test_login_success -v
```

## Development

### Code Quality

```bash
# Format code
black app tests

# Sort imports
isort app tests

# Lint code
ruff check app tests

# Type checking
mypy app
```

### Database Operations

```bash
# Drop all tables and recreate (CAUTION: DATA LOSS!)
alembic downgrade base
alembic upgrade head

# Reset test database
pytest --create-db
```

## Docker Support

### Using Docker Compose

```bash
# Build and start services
docker-compose up -d

# Run migrations
docker-compose exec api alembic upgrade head

# View logs
docker-compose logs -f api

# Stop services
docker-compose down
```

## Security

### Best Practices

1. **Environment Variables**: Never commit `.env` file
2. **Secret Key**: Use strong random key (32+ characters)
3. **HTTPS**: Always use HTTPS in production
4. **Database**: Use strong passwords and restrict access
5. **Token Storage**: Store tokens securely on client side
6. **CORS**: Configure appropriate CORS origins
7. **Rate Limiting**: Implement rate limiting for auth endpoints

### Password Requirements

- Minimum 8 characters
- Automatically hashed with bcrypt

### Token Expiration

- Access Token: 30 minutes (configurable)
- Refresh Token: 7 days

## API Usage Examples

### Register a User

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "johndoe",
    "password": "securepassword123"
  }'
```

### Login

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'
```

### Access Protected Endpoint

```bash
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer <access_token>"
```

## Troubleshooting

### Database Connection Issues

```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql

# Check database exists
sudo -u postgres psql -l

# Test connection
psql -U ssvproff_user -d ssvproff_db -h localhost
```

### Migration Issues

```bash
# Check current revision
alembic current

# Stamp database with latest revision (if out of sync)
alembic stamp head

# Show migration history
alembic history
```

### Import Errors

```bash
# Ensure you're in the correct directory
cd api

# Reinstall dependencies
pip install -r requirements.txt
```

## Contributing

1. Follow the existing code style
2. Write tests for new features
3. Update documentation
4. Ensure all tests pass
5. Run code quality tools

## Documentation

- [Authentication API](docs/authentication.md) - Complete authentication API reference
- [Database Setup](docs/database_setup.md) - Database configuration and migration guide
- [API Docs (Swagger)](http://localhost:8000/docs) - Interactive API documentation
- [API Docs (ReDoc)](http://localhost:8000/redoc) - Alternative API documentation

## Tech Stack

- **Framework**: FastAPI 0.115+
- **Database**: PostgreSQL with SQLAlchemy 2.0+
- **Authentication**: JWT with python-jose
- **Password Hashing**: passlib with bcrypt
- **Migrations**: Alembic 1.12+
- **Testing**: pytest with httpx
- **Validation**: Pydantic 2.0+
- **Type Checking**: mypy
- **Code Quality**: ruff, black, isort

## License

See the LICENSE file in the root of the repository.

## Support

For issues and questions:
1. Check the documentation
2. Review existing GitHub issues
3. Create a new issue with detailed information

---

**Note**: This is the API component of the SSVproff monorepo. See the root README for overall project information.
