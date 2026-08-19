"""add purchase records

Revision ID: 9f0a1b2c3d4e
Revises: 8e9f0a1b2c3d
Create Date: 2026-08-19 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = "9f0a1b2c3d4e"
down_revision = "8e9f0a1b2c3d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    if sa.inspect(op.get_bind()).has_table("purchase_records"):
        return

    op.create_table(
        "purchase_records",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("customer_id", sa.String(length=20), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column("unit_price", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column("amount", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column("paid", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["customer_id"], ["customers.customer_id"]),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_purchase_records_id"), "purchase_records", ["id"], unique=False)
    op.create_index(op.f("ix_purchase_records_customer_id"), "purchase_records", ["customer_id"], unique=False)
    op.create_index(op.f("ix_purchase_records_product_id"), "purchase_records", ["product_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_purchase_records_product_id"), table_name="purchase_records")
    op.drop_index(op.f("ix_purchase_records_customer_id"), table_name="purchase_records")
    op.drop_index(op.f("ix_purchase_records_id"), table_name="purchase_records")
    op.drop_table("purchase_records")
