"""Added a column to the Lottery table for base_64 encoded PDF

Revision ID: 3992b6e64d18
Revises: b69834d07b20
Create Date: 2018-11-07 23:54:45.010383

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3992b6e64d18'
down_revision = 'b69834d07b20'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('lotteries', sa.Column('pdf_base_64', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('lotteries', 'pdf_base_64')
    # ### end Alembic commands ###
