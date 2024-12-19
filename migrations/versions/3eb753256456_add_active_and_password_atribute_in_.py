"""Add active and password atribute in user db.

Revision ID: 3eb753256456
Revises: 33d95f888ccd
Create Date: 2024-12-17 08:26:30.996729

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3eb753256456'
down_revision = '33d95f888ccd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('active', sa.Boolean(), nullable=False))
        batch_op.add_column(sa.Column('password', sa.String(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('password')
        batch_op.drop_column('active')

    # ### end Alembic commands ###