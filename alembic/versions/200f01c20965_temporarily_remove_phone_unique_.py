"""temporarily_remove_phone_unique_constraint_for_testing

Revision ID: 200f01c20965
Revises: e63c35b6989b
Create Date: 2025-11-08 15:15:03.437730

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '200f01c20965'
down_revision: Union[str, None] = 'e63c35b6989b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    TEMPORARY: Remove phone unique constraint for testing.

    This allows multiple test users to have the same phone number
    for dry run testing of SMS rotation.

    TODO: Run downgrade() before production deployment to restore uniqueness!
    """
    # Drop the unique index on phone
    op.drop_index('ix_team_members_phone', table_name='team_members')

    # Re-create as non-unique index
    op.create_index('ix_team_members_phone', 'team_members', ['phone'], unique=False)


def downgrade() -> None:
    """
    Restore phone unique constraint.

    Run this before production deployment to restore phone uniqueness!
    """
    # Drop the non-unique index
    op.drop_index('ix_team_members_phone', table_name='team_members')

    # Re-create as unique index
    op.create_index('ix_team_members_phone', 'team_members', ['phone'], unique=True)
