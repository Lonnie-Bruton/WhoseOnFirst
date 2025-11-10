"""fix notification log cascade delete preserve audit trail

Revision ID: aea7552f1a21
Revises: e1f19bda1b9d
Create Date: 2025-11-10 17:23:55.041692

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aea7552f1a21'
down_revision: Union[str, None] = 'e1f19bda1b9d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Fix notification_log to preserve audit trail on schedule deletion
    # Make schedule_id nullable and change CASCADE to SET NULL
    # For SQLite, we need to recreate the table manually to change FK constraints

    # Step 1: Create temporary table with correct schema
    op.create_table('notification_log_new',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('schedule_id', sa.Integer(), nullable=True),  # Made nullable
        sa.Column('sent_at', sa.DateTime(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('twilio_sid', sa.String(), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('recipient_name', sa.String(length=100), nullable=True),
        sa.Column('recipient_phone', sa.String(length=15), nullable=True),
        sa.ForeignKeyConstraint(['schedule_id'], ['schedule.id'], ondelete='SET NULL'),  # Changed to SET NULL
        sa.PrimaryKeyConstraint('id')
    )

    # Step 2: Copy data from old table to new table
    op.execute('''
        INSERT INTO notification_log_new
        (id, schedule_id, sent_at, status, twilio_sid, error_message, recipient_name, recipient_phone)
        SELECT id, schedule_id, sent_at, status, twilio_sid, error_message, recipient_name, recipient_phone
        FROM notification_log
    ''')

    # Step 3: Drop old table
    op.drop_table('notification_log')

    # Step 4: Rename new table to original name
    op.rename_table('notification_log_new', 'notification_log')

    # Step 5: Recreate indexes
    op.create_index(op.f('ix_notification_log_id'), 'notification_log', ['id'], unique=False)
    op.create_index(op.f('ix_notification_log_schedule_id'), 'notification_log', ['schedule_id'], unique=False)
    op.create_index(op.f('ix_notification_log_sent_at'), 'notification_log', ['sent_at'], unique=False)
    op.create_index(op.f('ix_notification_log_status'), 'notification_log', ['status'], unique=False)


def downgrade() -> None:
    # Revert to CASCADE delete (not recommended for production)
    # WARNING: This will fail if notification_log contains NULL schedule_id values!

    # Step 1: Create temporary table with old schema
    op.create_table('notification_log_old',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('schedule_id', sa.Integer(), nullable=False),  # Back to non-nullable
        sa.Column('sent_at', sa.DateTime(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('twilio_sid', sa.String(), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('recipient_name', sa.String(length=100), nullable=True),
        sa.Column('recipient_phone', sa.String(length=15), nullable=True),
        sa.ForeignKeyConstraint(['schedule_id'], ['schedule.id'], ondelete='CASCADE'),  # Back to CASCADE
        sa.PrimaryKeyConstraint('id')
    )

    # Step 2: Copy data (will fail if NULL values exist)
    op.execute('''
        INSERT INTO notification_log_old
        (id, schedule_id, sent_at, status, twilio_sid, error_message, recipient_name, recipient_phone)
        SELECT id, schedule_id, sent_at, status, twilio_sid, error_message, recipient_name, recipient_phone
        FROM notification_log
        WHERE schedule_id IS NOT NULL
    ''')

    # Step 3: Drop current table
    op.drop_table('notification_log')

    # Step 4: Rename temp table to original name
    op.rename_table('notification_log_old', 'notification_log')

    # Step 5: Recreate indexes
    op.create_index(op.f('ix_notification_log_id'), 'notification_log', ['id'], unique=False)
    op.create_index(op.f('ix_notification_log_schedule_id'), 'notification_log', ['schedule_id'], unique=False)
    op.create_index(op.f('ix_notification_log_sent_at'), 'notification_log', ['sent_at'], unique=False)
    op.create_index(op.f('ix_notification_log_status'), 'notification_log', ['status'], unique=False)
