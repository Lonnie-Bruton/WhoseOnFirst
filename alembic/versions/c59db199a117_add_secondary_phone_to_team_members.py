"""add_secondary_phone_to_team_members

Revision ID: c59db199a117
Revises: aea7552f1a21
Create Date: 2025-11-17 21:35:01.098379

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c59db199a117'
down_revision: Union[str, None] = 'aea7552f1a21'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Add optional secondary_phone column for dual-device paging.

    This allows team members to receive SMS notifications on both
    office phone (primary) and personal phone (secondary) for redundancy.

    NOTE: Compatible with testing mode (migration 200f01c20965) where
    multiple team members can share the same phone number.
    """
    # Add nullable secondary_phone column (no unique constraint)
    op.add_column('team_members', sa.Column('secondary_phone', sa.String(length=15), nullable=True))


def downgrade() -> None:
    """
    Remove secondary_phone column.
    """
    op.drop_column('team_members', 'secondary_phone')
