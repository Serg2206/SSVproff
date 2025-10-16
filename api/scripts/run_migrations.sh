
#!/bin/bash
# Run Alembic migrations

set -e

echo "Running database migrations..."

# Change to the api directory
cd "$(dirname "$0")/.."

# Run migrations
python -m alembic upgrade head

echo "✓ Migrations completed successfully!"

