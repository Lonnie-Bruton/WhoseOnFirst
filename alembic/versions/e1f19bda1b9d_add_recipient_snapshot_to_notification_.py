"""add recipient snapshot to notification log

Revision ID: e1f19bda1b9d
Revises: 5403b6c7160f
Create Date: 2025-11-10 17:06:29.570809

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e1f19bda1b9d'
down_revision: Union[str, None] = '5403b6c7160f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add recipient snapshot columns to preserve historical notification data
    op.add_column('notification_log', sa.Column('recipient_name', sa.String(length=100), nullable=True))
    op.add_column('notification_log', sa.Column('recipient_phone', sa.String(length=15), nullable=True))


def downgrade() -> None:
    # Remove recipient snapshot columns
    op.drop_column('notification_log', 'recipient_phone')
    op.drop_column('notification_log', 'recipient_name')
