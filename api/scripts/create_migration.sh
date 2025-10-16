
#!/bin/bash
# Create a new Alembic migration

set -e

if [ -z "$1" ]; then
    echo "Usage: $0 <migration_message>"
    echo "Example: $0 'add_user_table'"
    exit 1
fi

echo "Creating new migration: $1"

# Change to the api directory
cd "$(dirname "$0")/.."

# Create migration
python -m alembic revision --autogenerate -m "$1"

echo "✓ Migration created successfully!"
echo "Don't forget to review the generated migration file before running it."

