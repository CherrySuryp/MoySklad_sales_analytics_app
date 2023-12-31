"""empty message

Revision ID: ce396644afc2
Revises: 
Create Date: 2023-07-12 23:28:53.074875

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ce396644afc2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('date_registered', sa.Date(), nullable=True),
    sa.Column('ms_token', sa.String(), nullable=True),
    sa.Column('telegram_id', sa.Integer(), nullable=True),
    sa.Column('verified', sa.Boolean(), nullable=False),
    sa.Column('items_limit', sa.Integer(), nullable=False),
    sa.Column('max_time_range', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('items',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('item_code', sa.String(), nullable=False),
    sa.Column('item_external_code', sa.String(), nullable=False),
    sa.Column('item_name', sa.String(), nullable=False),
    sa.Column('ms_id', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('ms_id')
    )
    op.create_table('orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ms_id', sa.String(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('order_name', sa.String(), nullable=False),
    sa.Column('order_date', sa.Date(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('ms_id')
    )
    op.create_table('order_details',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_ms_id', sa.String(), nullable=False),
    sa.Column('product_ms_id', sa.String(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('sum', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['order_ms_id'], ['orders.ms_id'], ),
    sa.ForeignKeyConstraint(['product_ms_id'], ['items.ms_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('order_details')
    op.drop_table('orders')
    op.drop_table('items')
    op.drop_table('users')
    # ### end Alembic commands ###
