# Authentication System Setup Guide

## 📋 Overview

This guide provides complete setup instructions for the SSVproff authentication system, which includes:

- **Backend (FastAPI)**: JWT-based authentication with PostgreSQL/SQLite
- **Frontend (Next.js)**: React context-based auth with protected routes
- **Example Resources**: Task management CRUD operations

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL (optional, SQLite works for development)

### 1. Backend Setup

```bash
cd api

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env

# For development with SQLite (no PostgreSQL required):
# Edit .env and set: DATABASE_URL=sqlite:///./ssvproff_dev.db

# For PostgreSQL:
# Edit .env and set: DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# Generate a secure secret key
openssl rand -hex 32
# Copy the output and set it as SECRET_KEY in .env

# Initialize database (creates tables and test users)
python scripts/init_db.py

# Or use Alembic migrations (recommended for production)
alembic upgrade head

# Run the API
uvicorn app.main:app --reload --port 8000
```

The API will be available at:
- API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 2. Frontend Setup

```bash
cd web

# Install dependencies
npm install

# Configure environment
cp .env.local.example .env.local

# Run development server
npm run dev
```

The web app will be available at http://localhost:3000

## 👤 Test Accounts

The `init_db.py` script creates two test accounts:

### Regular User
- **Email**: test@example.com
- **Password**: testpassword123

### Admin User (Superuser)
- **Email**: admin@example.com
- **Password**: admin123
- ⚠️ **Change this password in production!**

## 📖 Features

### Backend Features

1. **User Management**
   - User registration with email and username
   - Secure password hashing (bcrypt)
   - User profile endpoints

2. **Authentication**
   - JWT access tokens (30 min expiry)
   - JWT refresh tokens (7 day expiry)
   - Token refresh endpoint

3. **Protected Resources**
   - Example Task CRUD operations
   - User-specific data isolation
   - Role-based access (is_superuser flag)

4. **Database**
   - SQLAlchemy ORM
   - Alembic migrations
   - PostgreSQL and SQLite support
   - UUID primary keys
   - Optimized indexes

### Frontend Features

1. **Authentication UI**
   - Login page
   - Registration page
   - Password validation
   - Error handling

2. **Protected Routes**
   - Automatic redirect to login
   - Loading states
   - Auth context provider

3. **User Dashboard**
   - Task management (create, read, update, delete)
   - Filter tasks (all, active, completed)
   - User profile page

4. **State Management**
   - React Context for auth state
   - Persistent sessions (localStorage)
   - Automatic token injection

## 🔧 API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/v1/auth/register` | Register new user | No |
| POST | `/api/v1/auth/login` | Login user | No |
| GET | `/api/v1/auth/me` | Get current user | Yes |
| POST | `/api/v1/auth/refresh` | Refresh access token | No |

### Tasks (Example Protected Resource)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/v1/tasks/` | List user's tasks | Yes |
| POST | `/api/v1/tasks/` | Create new task | Yes |
| GET | `/api/v1/tasks/{id}` | Get specific task | Yes |
| PUT | `/api/v1/tasks/{id}` | Update task | Yes |
| DELETE | `/api/v1/tasks/{id}` | Delete task | Yes |

## 📝 Usage Examples

### Registration

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newuser@example.com",
    "username": "newuser",
    "password": "securepassword123"
  }'
```

### Login

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpassword123"
  }'
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Create Task (Protected)

```bash
curl -X POST "http://localhost:8000/api/v1/tasks/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete documentation",
    "description": "Write comprehensive docs",
    "is_completed": false
  }'
```

## 🧪 Testing

### Backend Tests

```bash
cd api

# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_auth_endpoints.py -v

# Run specific test
pytest tests/test_auth_endpoints.py::TestLoginEndpoint::test_login_success -v
```

Test coverage includes:
- ✅ User registration (success, duplicates, validation)
- ✅ User login (success, wrong password, nonexistent user)
- ✅ Token validation (valid, invalid, expired)
- ✅ Token refresh (success, invalid tokens)
- ✅ Protected endpoints (with/without auth)
- ✅ Task CRUD operations (all methods)
- ✅ User data isolation

### Frontend Tests

```bash
cd web

# Run tests
npm test

# Run with coverage
npm run test:coverage

# Watch mode
npm run test:watch
```

## 🛠️ Database Management

### Using Alembic (Recommended)

```bash
cd api

# Run migrations
alembic upgrade head

# Create new migration
alembic revision --autogenerate -m "description"

# Rollback one version
alembic downgrade -1

# Show current version
alembic current

# Show migration history
alembic history
```

### Helper Scripts

```bash
cd api

# Initialize database with test users
python scripts/init_db.py

# Run migrations (wrapper script)
./scripts/run_migrations.sh

# Create new migration (wrapper script)
./scripts/create_migration.sh "add_new_table"
```

## 🔒 Security Best Practices

### Environment Variables

1. **Never commit `.env` files**
   - Already in `.gitignore`
   - Use `.env.example` as template

2. **Generate strong SECRET_KEY**
   ```bash
   openssl rand -hex 32
   ```

3. **Use environment-specific values**
   - Development: SQLite, debug mode
   - Production: PostgreSQL, HTTPS, strong passwords

### Password Requirements

- Minimum 8 characters
- Alphanumeric + special characters recommended
- Hashed with bcrypt (never stored as plain text)

### Token Security

- Access tokens: 30 minutes (short-lived)
- Refresh tokens: 7 days (longer-lived)
- Store securely on client (httpOnly cookies recommended for production)
- Always use HTTPS in production

### CORS Configuration

Update `BACKEND_CORS_ORIGINS` in `.env`:
```env
BACKEND_CORS_ORIGINS=["http://localhost:3000", "https://yourdomain.com"]
```

## 📚 Documentation

Comprehensive documentation is available:

- **API Authentication**: [`api/docs/AUTHENTICATION.md`](api/docs/AUTHENTICATION.md)
- **Web Authentication**: [`web/docs/AUTHENTICATION.md`](web/docs/AUTHENTICATION.md)
- **API Docs**: http://localhost:8000/docs (when running)

## 🐛 Troubleshooting

### Database Connection Issues

**Problem**: `connection refused` error

**Solution**: Use SQLite for development:
```env
DATABASE_URL=sqlite:///./ssvproff_dev.db
```

### Import Errors

**Problem**: `ModuleNotFoundError: No module named 'app'`

**Solution**: Run commands from the `api/` directory

### Token Validation Errors

**Problem**: `Could not validate credentials`

**Solutions**:
1. Check if `SECRET_KEY` is set correctly
2. Ensure token hasn't expired
3. Verify token format: `Bearer <token>`

### CORS Errors

**Problem**: Browser blocks API requests

**Solution**: Add frontend URL to `BACKEND_CORS_ORIGINS` in API `.env`

### Frontend Not Connecting to API

**Problem**: API calls fail with network error

**Solutions**:
1. Check API is running: `curl http://localhost:8000/health`
2. Verify `NEXT_PUBLIC_API_URL` in `web/.env.local`
3. Check browser console for CORS errors

## 🚀 Production Deployment

### Backend

1. **Set environment variables**
   ```env
   DEBUG=false
   DATABASE_URL=postgresql://user:pass@host:5432/db
   SECRET_KEY=<generate-strong-key>
   BACKEND_CORS_ORIGINS=["https://yourdomain.com"]
   ```

2. **Run migrations**
   ```bash
   alembic upgrade head
   ```

3. **Use production server**
   ```bash
   gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

### Frontend

1. **Set environment variable**
   ```env
   NEXT_PUBLIC_API_URL=https://api.yourdomain.com/api/v1
   ```

2. **Build and deploy**
   ```bash
   npm run build
   npm start
   # Or deploy to Vercel/Netlify
   ```

## 📦 Project Structure

```
SSVproff/
├── api/                          # FastAPI backend
│   ├── app/
│   │   ├── api/                  # API endpoints
│   │   │   └── v1/
│   │   │       ├── endpoints/    # Route handlers
│   │   │       │   ├── auth.py   # Auth endpoints
│   │   │       │   ├── tasks.py  # Task endpoints
│   │   │       │   └── health.py
│   │   │       └── api.py        # Router aggregator
│   │   ├── core/                 # Core utilities
│   │   │   ├── config.py         # Settings
│   │   │   └── security.py       # JWT & passwords
│   │   ├── db/                   # Database
│   │   │   ├── base.py           # Base model
│   │   │   └── session.py        # DB session
│   │   ├── models/               # SQLAlchemy models
│   │   │   ├── user.py
│   │   │   └── task.py
│   │   ├── schemas/              # Pydantic schemas
│   │   │   ├── user.py
│   │   │   ├── auth.py
│   │   │   └── task.py
│   │   └── services/             # Business logic
│   │       ├── auth.py
│   │       └── task.py
│   ├── alembic/                  # Database migrations
│   ├── scripts/                  # Utility scripts
│   │   ├── init_db.py
│   │   ├── run_migrations.sh
│   │   └── create_migration.sh
│   ├── tests/                    # Test suite
│   └── docs/                     # Documentation
│
└── web/                          # Next.js frontend
    ├── src/
    │   ├── components/           # React components
    │   │   └── ProtectedRoute.tsx
    │   ├── contexts/             # React contexts
    │   │   └── AuthContext.tsx
    │   ├── lib/                  # Utilities
    │   │   ├── api.ts            # API client
    │   │   └── auth.ts           # Auth utilities
    │   ├── pages/                # Next.js pages
    │   │   ├── index.tsx         # Home
    │   │   ├── login.tsx         # Login page
    │   │   ├── register.tsx      # Register page
    │   │   ├── dashboard.tsx     # Dashboard
    │   │   ├── profile.tsx       # Profile
    │   │   └── _app.tsx          # App wrapper
    │   └── styles/               # CSS modules
    └── docs/                     # Documentation
```

## 🤝 Contributing

When extending the authentication system:

1. Follow existing patterns
2. Add tests for new endpoints
3. Update documentation
4. Run linters: `pytest`, `npm run lint`

## 📄 License

MIT License - See LICENSE file for details

## 💡 Support

For issues or questions:
1. Check troubleshooting section
2. Review documentation in `docs/`
3. Check API docs at `/docs`
4. Open an issue on GitHub

---

**Happy coding! 🎉**
