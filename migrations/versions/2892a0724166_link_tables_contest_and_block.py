"""Link tables: Contest and Block

Revision ID: 2892a0724166
Revises: 8c4e132224eb
Create Date: 2020-10-19 00:18:16.947272

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2892a0724166'
down_revision = '8c4e132224eb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('block',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=32), nullable=True),
    sa.Column('desc', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('contest_block_rel',
    sa.Column('contest_id', sa.Integer(), nullable=True),
    sa.Column('block_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['block_id'], ['block.id'], ),
    sa.ForeignKeyConstraint(['contest_id'], ['contest.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('contest_block_rel')
    op.drop_table('block')
    # ### end Alembic commands ###
