"""Create Team table

Revision ID: 2ba81abb3f2c
Revises: 903101d5dc11
Create Date: 2020-10-29 04:53:51.387808

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2ba81abb3f2c'
down_revision = '903101d5dc11'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('team',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=32), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('team_mentor_rel',
    sa.Column('team_id', sa.Integer(), nullable=True),
    sa.Column('mentor_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['mentor_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['team_id'], ['team.id'], )
    )
    op.create_table('team_student_rel',
    sa.Column('team_id', sa.Integer(), nullable=True),
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['student_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['team_id'], ['team.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('team_student_rel')
    op.drop_table('team_mentor_rel')
    op.drop_table('team')
    # ### end Alembic commands ###