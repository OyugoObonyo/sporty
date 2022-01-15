"""Add models

Revision ID: 960ed1e0ff8b
Revises: 
Create Date: 2022-01-14 17:53:11.846178

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '960ed1e0ff8b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=40), nullable=False),
    sa.Column('email', sa.String(length=40), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_id'), ['id'], unique=False)

    op.create_table('product',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=40), nullable=False),
    sa.Column('image_file', sa.String(length=40), nullable=True),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('date_posted', sa.DateTime(), nullable=True),
    sa.Column('vendor_id', sa.Integer(), nullable=True),
    sa.Column('brand', sa.String(length=12), nullable=True),
    sa.Column('category', sa.String(length=12), nullable=True),
    sa.ForeignKeyConstraint(['vendor_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_product_date_posted'), ['date_posted'], unique=False)
        batch_op.create_index(batch_op.f('ix_product_id'), ['id'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_product_id'))
        batch_op.drop_index(batch_op.f('ix_product_date_posted'))

    op.drop_table('product')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_id'))

    op.drop_table('user')
    # ### end Alembic commands ###