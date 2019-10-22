"""empty message

Revision ID: bcad9f8f3ddb
Revises: b958d9127d6d
Create Date: 2019-10-17 12:30:15.998400

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bcad9f8f3ddb'
down_revision = 'b958d9127d6d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('employee_detail',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('employee_id', sa.Integer(), nullable=True),
    sa.Column('plantilla_id', sa.Integer(), nullable=True),
    sa.Column('salary_id', sa.Integer(), nullable=True),
    sa.Column('assigned_office_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['assigned_office_id'], ['office.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['employee_id'], ['employee.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['plantilla_id'], ['plantilla.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['salary_id'], ['salary.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('employee_detail')
    # ### end Alembic commands ###
