"""Create tasks table

Revision ID: 6d8f24eb9dd2
Revises: 5c4913ea8cc1
Create Date: 2025-10-16 21:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision: str = '6d8f24eb9dd2'
down_revision: Union[str, Sequence[str], None] = '5c4913ea8cc1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema - create tasks table."""
    op.create_table(
        'tasks',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_completed', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('owner_id', UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ondelete='CASCADE')
    )
    
    # Create indexes
    op.create_index('ix_tasks_id', 'tasks', ['id'])
    op.create_index('ix_tasks_owner_id', 'tasks', ['owner_id'])
    op.create_index('ix_tasks_owner_completed', 'tasks', ['owner_id', 'is_completed'])
    op.create_index('ix_tasks_owner_created', 'tasks', ['owner_id', 'created_at'])


def downgrade() -> None:
    """Downgrade schema - drop tasks table."""
    op.drop_index('ix_tasks_owner_created', table_name='tasks')
    op.drop_index('ix_tasks_owner_completed', table_name='tasks')
    op.drop_index('ix_tasks_owner_id', table_name='tasks')
    op.drop_index('ix_tasks_id', table_name='tasks')
    op.drop_table('tasks')
