"""empty message

Revision ID: 6aa7a86a9ce1
Revises: 899e20eba205
Create Date: 2017-09-12 07:08:05.966281

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6aa7a86a9ce1'
down_revision = '899e20eba205'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('user', sa.Column('active_repository_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_user_active_repository_id', 'user', 'repository', ['active_repository_id'], ['id'])
    

def downgrade():
    op.drop_constraint('fk_user_active_repository_id', 'user', type_='foreignkey')
    op.drop_column('user', 'active_repository_id')
    