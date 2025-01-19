"""Add genres column to Venue

Revision ID: 4476053e80f4
Revises: 87e2d21a0895
Create Date: 2025-01-03 22:06:26.084731

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '4476053e80f4'
down_revision = '87e2d21a0895'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('Venue', sa.Column('genres', sa.String(), nullable=True))

def downgrade():
    op.drop_column('Venue', 'genres')

    # ### end Alembic commands ###
