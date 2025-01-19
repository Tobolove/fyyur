"""added more details

Revision ID: d7e199d52b30
Revises: 88d8420c53fb
Create Date: 2025-01-04 16:23:33.800969

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd7e199d52b30'
down_revision = '88d8420c53fb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Artist', schema=None) as batch_op:
        batch_op.alter_column('image_link',
               existing_type=sa.VARCHAR(length=500),
               type_=sa.String(length=5000),
               existing_nullable=True)

    with op.batch_alter_table('Venue', schema=None) as batch_op:
        batch_op.alter_column('website_link',
               existing_type=sa.VARCHAR(length=5000),
               type_=sa.String(length=120),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Venue', schema=None) as batch_op:
        batch_op.alter_column('website_link',
               existing_type=sa.String(length=120),
               type_=sa.VARCHAR(length=5000),
               existing_nullable=True)

    with op.batch_alter_table('Artist', schema=None) as batch_op:
        batch_op.alter_column('image_link',
               existing_type=sa.String(length=5000),
               type_=sa.VARCHAR(length=500),
               existing_nullable=True)

    # ### end Alembic commands ###
