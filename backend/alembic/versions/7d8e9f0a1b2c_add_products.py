"""add products

Revision ID: 7d8e9f0a1b2c
Revises: 3bc54d4390c9
Create Date: 2026-08-19 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = "7d8e9f0a1b2c"
down_revision = "3bc54d4390c9"
branch_labels = None
depends_on = None


def upgrade() -> None:
    if sa.inspect(op.get_bind()).has_table("products"):
        return

    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("product_name", sa.String(length=150), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("quantity", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column("size", sa.String(length=50), nullable=True),
        sa.Column("price", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_products_id"), "products", ["id"], unique=False)
    op.create_index(op.f("ix_products_product_name"), "products", ["product_name"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_products_product_name"), table_name="products")
    op.drop_index(op.f("ix_products_id"), table_name="products")
    op.drop_table("products")
