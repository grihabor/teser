"""empty message

Revision ID: fd05599e10a6
Revises: 8a04dc559206
Create Date: 2017-08-22 14:26:50.486659

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fd05599e10a6'
down_revision = '8a04dc559206'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('repository', sa.Column('identity_file', sa.String(length=255), nullable=False))


def downgrade():
    op.drop_column('repository', 'identity_file')
