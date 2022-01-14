"""Remove uuids from models

Revision ID: 457c94d9bac9
Revises: b715a66787c5
Create Date: 2022-01-14 14:14:12.187410

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '457c94d9bac9'
down_revision = 'b715a66787c5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.drop_column('prod_uuid')

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('user_uuid')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_uuid', sa.VARCHAR(length=36), nullable=True))

    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.add_column(sa.Column('prod_uuid', sa.VARCHAR(length=36), nullable=True))

    # ### end Alembic commands ###