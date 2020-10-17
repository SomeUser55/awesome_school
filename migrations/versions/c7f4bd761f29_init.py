"""Init

Revision ID: c7f4bd761f29
Revises: 
Create Date: 2020-10-17 21:01:07.383118

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils

# revision identifiers, used by Alembic.
revision = 'c7f4bd761f29'
down_revision = None
branch_labels = None
depends_on = None

from main_app import models

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contest',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=32), nullable=True),
    sa.Column('desc', sa.Text(), nullable=True),
    sa.Column('unit_test', sa.Text(), nullable=True),
    sa.Column('lang', sqlalchemy_utils.types.choice.ChoiceType(models.Contest.LANGS), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=32), nullable=True),
    sa.Column('second_name', sa.String(length=32), nullable=True),
    sa.Column('email', sa.String(length=32), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_email'), ['email'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_email'))

    op.drop_table('user')
    op.drop_table('contest')
    # ### end Alembic commands ###
