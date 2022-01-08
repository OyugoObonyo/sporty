"""Edit image_file column

Revision ID: bf54c5b5c712
Revises: 40ce9561672f
Create Date: 2022-01-08 14:56:04.089238

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bf54c5b5c712'
down_revision = '40ce9561672f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('_alembic_tmp_product')
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image_file', sa.String(length=40), nullable=True))
        batch_op.drop_column('image')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image', sa.VARCHAR(length=40), nullable=True))
        batch_op.drop_column('image_file')

    op.create_table('_alembic_tmp_product',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=40), nullable=False),
    sa.Column('description', sa.VARCHAR(length=120), nullable=False),
    sa.Column('price', sa.INTEGER(), nullable=False),
    sa.Column('date_posted', sa.DATETIME(), nullable=True),
    sa.Column('vendor_id', sa.INTEGER(), nullable=True),
    sa.Column('brand_id', sa.INTEGER(), nullable=True),
    sa.Column('category_id', sa.INTEGER(), nullable=True),
    sa.Column('image', sa.VARCHAR(length=40), nullable=False),
    sa.ForeignKeyConstraint(['brand_id'], ['brand.id'], ),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
    sa.ForeignKeyConstraint(['vendor_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###