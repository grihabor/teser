"""Initial commit

Revision ID: 8a04dc559206
Revises: 
Create Date: 2017-08-20 00:29:14.616856

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '8a04dc559206'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'role',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=80), nullable=True),
        sa.Column('description', sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('username', sa.String(length=255), nullable=True),
        sa.Column('password', sa.String(length=255), nullable=True),
        sa.Column('last_login_at', sa.DateTime(), nullable=True),
        sa.Column('current_login_at', sa.DateTime(), nullable=True),
        sa.Column('last_login_ip', sa.String(length=100), nullable=True),
        sa.Column('current_login_ip', sa.String(length=100), nullable=True),
        sa.Column('login_count', sa.Integer(), nullable=True),
        sa.Column('active', sa.Boolean(), nullable=True),
        sa.Column('confirmed_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    op.create_table(
        'repository',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('url', sa.String(length=2000), nullable=False),
        sa.Column('branch', sa.String(length=255), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'roles_users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('role_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('roles_users')
    op.drop_table('repository')
    op.drop_table('user')
    op.drop_table('role')
