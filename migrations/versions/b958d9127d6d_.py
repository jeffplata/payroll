"""empty message

Revision ID: b958d9127d6d
Revises: 9d9316d0c52f
Create Date: 2019-10-14 17:06:43.644938

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b958d9127d6d'
down_revision = '9d9316d0c52f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('employee',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('employee_no', sa.String(length=20), nullable=True),
    sa.Column('last_name', sa.String(length=80), nullable=False),
    sa.Column('first_name', sa.String(length=80), nullable=False),
    sa.Column('middle_name', sa.String(length=80), nullable=True),
    sa.Column('birth_date', sa.DateTime(), nullable=True),
    sa.Column('etd_nfa', sa.DateTime(), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_modified', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('employee_no')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('employee')
    # ### end Alembic commands ###
