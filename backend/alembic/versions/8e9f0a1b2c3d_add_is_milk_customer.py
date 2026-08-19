"""add is milk customer flag

Revision ID: 8e9f0a1b2c3d
Revises: 7d8e9f0a1b2c
Create Date: 2026-08-19 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = "8e9f0a1b2c3d"
down_revision = "7d8e9f0a1b2c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "customers",
        sa.Column("is_milk_customer", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.alter_column("customers", "is_milk_customer", server_default=None)


def downgrade() -> None:
    op.drop_column("customers", "is_milk_customer")
