"""last_message table

Revision ID: c0bf9bc13378
Revises: 00ea57135dce
Create Date: 2018-11-03 19:20:30.177226

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c0bf9bc13378'
down_revision = '00ea57135dce'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('last_message',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('fb_id', sa.String(length=64), nullable=True),
    sa.Column('datetime', sa.DateTime(), nullable=True),
    sa.Column('text', sa.String(length=64), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('text'),
    mysql_engine='InnoDB'
    )
    op.create_index(op.f('ix_last_message_datetime'), 'last_message', ['datetime'], unique=False)
    op.create_index(op.f('ix_last_message_fb_id'), 'last_message', ['fb_id'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_last_message_fb_id'), table_name='last_message')
    op.drop_index(op.f('ix_last_message_datetime'), table_name='last_message')
    op.drop_table('last_message')
    # ### end Alembic commands ###