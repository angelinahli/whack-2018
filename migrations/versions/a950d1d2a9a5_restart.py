"""restart

Revision ID: a950d1d2a9a5
Revises: 
Create Date: 2018-11-04 01:45:35.321175

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a950d1d2a9a5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('intervention',
    sa.Column('intervention_id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(length=2048), nullable=True),
    sa.PrimaryKeyConstraint('intervention_id'),
    mysql_engine='InnoDB'
    )
    op.create_table('user',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('fb_id', sa.String(length=64), nullable=True),
    sa.Column('has_onboarded', sa.Boolean(), nullable=True),
    sa.Column('last_action', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('user_id'),
    mysql_engine='InnoDB'
    )
    op.create_index(op.f('ix_user_fb_id'), 'user', ['fb_id'], unique=True)
    op.create_index(op.f('ix_user_has_onboarded'), 'user', ['has_onboarded'], unique=False)
    op.create_index(op.f('ix_user_last_action'), 'user', ['last_action'], unique=False)
    op.create_table('Message',
    sa.Column('message_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('datetime', sa.DateTime(), nullable=True),
    sa.Column('text', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('message_id'),
    mysql_engine='InnoDB'
    )
    op.create_index(op.f('ix_Message_datetime'), 'Message', ['datetime'], unique=False)
    op.create_index(op.f('ix_Message_text'), 'Message', ['text'], unique=False)
    op.create_table('check_in',
    sa.Column('checkin_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('mid_checkin', sa.Boolean(), nullable=True),
    sa.Column('datetime', sa.DateTime(), nullable=True),
    sa.Column('baseline', sa.Integer(), nullable=True),
    sa.Column('tried_intervention', sa.Boolean(), nullable=True),
    sa.Column('intervention_id', sa.Integer(), nullable=True),
    sa.Column('impact', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['intervention_id'], ['intervention.intervention_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('checkin_id'),
    mysql_engine='InnoDB'
    )
    op.create_index(op.f('ix_check_in_baseline'), 'check_in', ['baseline'], unique=False)
    op.create_index(op.f('ix_check_in_datetime'), 'check_in', ['datetime'], unique=False)
    op.create_index(op.f('ix_check_in_impact'), 'check_in', ['impact'], unique=False)
    op.create_index(op.f('ix_check_in_mid_checkin'), 'check_in', ['mid_checkin'], unique=False)
    op.create_index(op.f('ix_check_in_tried_intervention'), 'check_in', ['tried_intervention'], unique=False)
    op.create_table('user_intervention',
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('intervention_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['intervention_id'], ['intervention.intervention_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('uid'),
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_intervention')
    op.drop_index(op.f('ix_check_in_tried_intervention'), table_name='check_in')
    op.drop_index(op.f('ix_check_in_mid_checkin'), table_name='check_in')
    op.drop_index(op.f('ix_check_in_impact'), table_name='check_in')
    op.drop_index(op.f('ix_check_in_datetime'), table_name='check_in')
    op.drop_index(op.f('ix_check_in_baseline'), table_name='check_in')
    op.drop_table('check_in')
    op.drop_index(op.f('ix_Message_text'), table_name='Message')
    op.drop_index(op.f('ix_Message_datetime'), table_name='Message')
    op.drop_table('Message')
    op.drop_index(op.f('ix_user_last_action'), table_name='user')
    op.drop_index(op.f('ix_user_has_onboarded'), table_name='user')
    op.drop_index(op.f('ix_user_fb_id'), table_name='user')
    op.drop_table('user')
    op.drop_table('intervention')
    # ### end Alembic commands ###
