"""role_type: not nullable and unique

Revision ID: 903101d5dc11
Revises: 6769e0afb610
Create Date: 2020-10-28 02:06:05.421074

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils



# revision identifiers, used by Alembic.
revision = '903101d5dc11'
down_revision = '6769e0afb610'
branch_labels = None
depends_on = None


ROLES = [
    (u'student', u'Student'),
    (u'mentor', u'Mentor'),
    (u'admin', u'Admin'),
]


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('role', schema=None) as batch_op:
        batch_op.add_column(sa.Column('role_type', sqlalchemy_utils.types.choice.ChoiceType(ROLES), nullable=False))
        batch_op.create_unique_constraint('role_type_constraint', ['role_type'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('role', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('role_type')

    # ### end Alembic commands ###
