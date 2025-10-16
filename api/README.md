
# SSVproff API

A comprehensive FastAPI-based backend for managing ML datasets, experiments, and projects.

## Features

- 🔐 JWT-based authentication
- 👥 User management
- 📁 Project organization
- 📊 Dataset management
- 🧪 Experiment tracking
- 📝 Complete API documentation
- 🔄 CORS support
- 💾 SQLite/PostgreSQL database support

## Quick Start

### Prerequisites

- Python 3.8+
- pip or poetry

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create environment file:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Initialize the database:
```bash
python init_db.py
```

This will create:
- All database tables
- A default admin user (username: `admin`, password: `admin123`)

**⚠️ Important: Change the admin password immediately after first login!**

### Running the Server

Development mode (with auto-reload):
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Production mode:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API will be available at:
- API: http://localhost:8000
- Interactive docs (Swagger): http://localhost:8000/docs
- Alternative docs (ReDoc): http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - Login and get access token
- `GET /api/v1/auth/me` - Get current user info

### Projects
- `GET /api/v1/projects` - List all projects
- `POST /api/v1/projects` - Create a new project
- `GET /api/v1/projects/{id}` - Get project details
- `PUT /api/v1/projects/{id}` - Update a project
- `DELETE /api/v1/projects/{id}` - Delete a project

### Health
- `GET /health` - Health check endpoint

## Project Structure

```
api/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI application
│   ├── config.py         # Configuration settings
│   ├── database.py       # Database connection
│   ├── models.py         # SQLAlchemy models
│   ├── schemas.py        # Pydantic schemas
│   ├── auth.py           # Authentication logic
│   └── routers/          # API route handlers
│       ├── __init__.py
│       ├── auth.py       # Auth endpoints
│       └── projects.py   # Project endpoints
├── init_db.py           # Database initialization script
├── requirements.txt     # Python dependencies
├── .env.example        # Environment variables template
└── README.md           # This file
```

## Configuration

Edit `.env` file to configure:
- Database connection
- JWT secret key
- Token expiration time
- CORS origins
- File upload settings

## Database

### SQLite (Default)
The default configuration uses SQLite, which is perfect for development and small deployments.

### PostgreSQL (Production)
For production, we recommend PostgreSQL:

1. Install PostgreSQL
2. Create a database:
```sql
CREATE DATABASE ssvproff;
```
3. Update `.env`:
```
DATABASE_URL=postgresql://user:password@localhost:5432/ssvproff
```

## Authentication

The API uses JWT (JSON Web Tokens) for authentication:

1. Register a new user or use the default admin account
2. Login to receive an access token
3. Include the token in subsequent requests:
```
Authorization: Bearer <your_token>
```

## Development

### Testing
```bash
pytest
```

### Code Formatting
```bash
black app/
```

### Linting
```bash
flake8 app/
```

## License

MIT License
