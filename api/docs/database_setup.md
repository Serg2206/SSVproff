
# Database Setup Guide

This guide explains how to set up and manage the PostgreSQL database for the SSVproff API.

## Prerequisites

- PostgreSQL 12 or higher
- Python 3.11+
- All dependencies from `requirements.txt` installed

## Quick Start

### 1. Install PostgreSQL

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

**macOS (using Homebrew):**
```bash
brew install postgresql@15
brew services start postgresql@15
```

**Windows:**
Download and install from [PostgreSQL Downloads](https://www.postgresql.org/download/windows/)

### 2. Create Database and User

```bash
# Access PostgreSQL as postgres user
sudo -u postgres psql

# Create database
CREATE DATABASE ssvproff_db;

# Create user
CREATE USER ssvproff_user WITH PASSWORD 'ssvproff_password';

# Grant privileges
GRANT ALL PRIVILEGES ON DATABASE ssvproff_db TO ssvproff_user;

# Exit psql
\q
```

### 3. Configure Environment

Update `api/.env` file with database URL:

```env
DATABASE_URL=postgresql://ssvproff_user:ssvproff_password@localhost:5432/ssvproff_db
```

### 4. Run Migrations

```bash
cd api
alembic upgrade head
```

## Database Configuration

### Connection URL Format

```
postgresql://username:password@host:port/database_name
```

**Examples:**

Local development:
```
postgresql://ssvproff_user:ssvproff_password@localhost:5432/ssvproff_db
```

Docker:
```
postgresql://ssvproff_user:ssvproff_password@db:5432/ssvproff_db
```

Remote server:
```
postgresql://user:password@db.example.com:5432/ssvproff_db
```

### Connection Pool Settings

The application uses SQLAlchemy's connection pooling:

- **Pool Size**: 5 permanent connections
- **Max Overflow**: 10 additional temporary connections
- **Pool Pre-Ping**: Enabled (verifies connections before use)
- **Pool Recycle**: 3600 seconds (1 hour)

These settings are configured in `app/db/session.py`.

## Alembic Migrations

### What is Alembic?

Alembic is a database migration tool for SQLAlchemy. It tracks database schema changes and allows versioned database upgrades/downgrades.

### Common Migration Commands

**Create a new migration:**
```bash
cd api
alembic revision -m "Description of changes"
```

**Auto-generate migration from models:**
```bash
cd api
alembic revision --autogenerate -m "Description of changes"
```
*Note: Requires database connection*

**Apply migrations:**
```bash
cd api
alembic upgrade head
```

**Downgrade one revision:**
```bash
cd api
alembic downgrade -1
```

**View migration history:**
```bash
cd api
alembic history
```

**View current revision:**
```bash
cd api
alembic current
```

### Migration File Structure

```
api/
├── alembic/
│   ├── versions/
│   │   └── 5c4913ea8cc1_create_users_table.py
│   ├── env.py           # Alembic environment configuration
│   ├── script.py.mako   # Migration template
│   └── README
├── alembic.ini          # Alembic configuration
└── app/
    └── db/
        └── base.py      # Import all models here
```

## Database Models

### User Model

Located in `app/models/user.py`

**Fields:**
- `id`: UUID primary key
- `email`: Unique email address (max 255 chars)
- `username`: Unique username (max 50 chars)
- `hashed_password`: Bcrypt hashed password (max 255 chars)
- `is_active`: Boolean flag for account status
- `is_superuser`: Boolean flag for admin privileges
- `created_at`: Timestamp of creation
- `updated_at`: Timestamp of last update

**Indexes:**
- Primary key on `id`
- Unique index on `email`
- Unique index on `username`
- Composite index on (`email`, `is_active`)
- Composite index on (`username`, `is_active`)

## Testing with Database

### Test Database Configuration

Tests use an in-memory SQLite database by default. This is configured in `tests/conftest.py`.

**Benefits:**
- Fast test execution
- No setup required
- Isolated from development database
- Automatic cleanup

### Running Tests

```bash
cd api
pytest
```

**Run specific test file:**
```bash
pytest tests/test_database.py
```

**Run with coverage:**
```bash
pytest --cov=app --cov-report=html
```

## Production Considerations

### Security

1. **Strong Passwords**: Use strong, random passwords for database users
2. **Network Security**: Restrict database access to application servers only
3. **SSL/TLS**: Enable SSL for database connections
4. **Regular Backups**: Implement automated backup strategy

### Performance

1. **Connection Pooling**: Already configured (adjust based on load)
2. **Indexes**: Review and add indexes for frequently queried fields
3. **Query Optimization**: Use EXPLAIN ANALYZE for slow queries
4. **Read Replicas**: Consider read replicas for high-traffic applications

### Monitoring

Monitor these metrics:
- Connection pool usage
- Query execution time
- Database size
- Index usage
- Lock contention

### Backup and Recovery

**Create backup:**
```bash
pg_dump -U ssvproff_user ssvproff_db > backup.sql
```

**Restore backup:**
```bash
psql -U ssvproff_user ssvproff_db < backup.sql
```

**Automated backups:**
Set up a cron job or use cloud provider's backup features.

## Docker Setup

### Docker Compose Configuration

Add to `docker-compose.yml`:

```yaml
services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: ssvproff_user
      POSTGRES_PASSWORD: ssvproff_password
      POSTGRES_DB: ssvproff_db
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ssvproff_user"]
      interval: 10s
      timeout: 5s
      retries: 5

  api:
    build: ./api
    depends_on:
      db:
        condition: service_healthy
    environment:
      DATABASE_URL: postgresql://ssvproff_user:ssvproff_password@db:5432/ssvproff_db

volumes:
  postgres_data:
```

### Initialize Database in Docker

```bash
# Start services
docker-compose up -d

# Run migrations
docker-compose exec api alembic upgrade head
```

## Troubleshooting

### Connection Refused

**Problem:** `connection to server at "localhost", port 5432 failed: Connection refused`

**Solutions:**
1. Check if PostgreSQL is running: `sudo systemctl status postgresql`
2. Verify connection URL in `.env`
3. Check PostgreSQL is listening on correct port: `sudo netstat -plunt | grep 5432`

### Authentication Failed

**Problem:** `FATAL: password authentication failed for user`

**Solutions:**
1. Verify username and password in DATABASE_URL
2. Check PostgreSQL user exists: `sudo -u postgres psql -c "\du"`
3. Reset password if needed

### Migration Errors

**Problem:** `Target database is not up to date`

**Solution:**
```bash
# Check current revision
alembic current

# Apply all migrations
alembic upgrade head
```

**Problem:** `Can't locate revision identified by 'xxxxx'`

**Solution:**
```bash
# Stamp database with current revision
alembic stamp head
```

## Additional Resources

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [FastAPI Database Guide](https://fastapi.tiangolo.com/tutorial/sql-databases/)
