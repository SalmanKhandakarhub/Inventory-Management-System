"""db migrations

Revision ID: 0c69969dd2c2
Revises: 
Create Date: 2024-07-25 17:41:11.476175

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0c69969dd2c2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('invoice',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('total_amount', sa.Float(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('product',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('category', sa.String(length=100), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('transaction',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('type', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('return',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('reason', sa.String(length=255), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['transaction.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sale',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('customer_id', sa.String(length=100), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['transaction.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('invoice_sale',
    sa.Column('invoice_id', sa.Integer(), nullable=False),
    sa.Column('sale_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['invoice_id'], ['invoice.id'], ),
    sa.ForeignKeyConstraint(['sale_id'], ['sale.id'], ),
    sa.PrimaryKeyConstraint('invoice_id', 'sale_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('invoice_sale')
    op.drop_table('sale')
    op.drop_table('return')
    op.drop_table('transaction')
    op.drop_table('product')
    op.drop_table('invoice')
    # ### end Alembic commands ###
