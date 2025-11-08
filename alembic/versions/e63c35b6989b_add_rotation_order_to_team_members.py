"""add_rotation_order_to_team_members

Revision ID: e63c35b6989b
Revises: 92999f654850
Create Date: 2025-11-08 14:21:36.447022

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e63c35b6989b'
down_revision: Union[str, None] = '92999f654850'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add rotation_order field to team_members table."""
    # Add rotation_order column (nullable to work with SQLite)
    # For existing rows, we'll populate with id to maintain current rotation order
    op.add_column('team_members', sa.Column('rotation_order', sa.Integer(), nullable=True))

    # Populate rotation_order with id for existing rows to maintain current order
    # This preserves the existing rotation behavior (sorted by ID)
    op.execute('UPDATE team_members SET rotation_order = id')

    # Add index for efficient sorting queries
    op.create_index(op.f('ix_team_members_rotation_order'), 'team_members', ['rotation_order'], unique=False)


def downgrade() -> None:
    """Remove rotation_order field from team_members table."""
    # Drop the index first
    op.drop_index(op.f('ix_team_members_rotation_order'), table_name='team_members')

    # Drop the column
    op.drop_column('team_members', 'rotation_order')
