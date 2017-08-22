"""empty message

Revision ID: 899e20eba205
Revises: fd05599e10a6
Create Date: 2017-08-22 15:19:57.733137

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '899e20eba205'
down_revision = 'fd05599e10a6'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('user', sa.Column('generated_identity_file', sa.String(length=255), nullable=True))


def downgrade():
    op.drop_column('user', 'generated_identity_file')
