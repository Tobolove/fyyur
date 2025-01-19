"""Step 1: added Shows and did all of the addings

Revision ID: 87e2d21a0895
Revises: 54b31173f12e
Create Date: 2025-01-03 15:49:17.286341

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '87e2d21a0895'
down_revision = '54b31173f12e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Show',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.Column('venue_id', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['artist_id'], ['Artist.id'], ),
    sa.ForeignKeyConstraint(['venue_id'], ['Venue.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('Artist', schema=None) as batch_op:
        batch_op.add_column(sa.Column('seeking_venue', sa.Boolean(), nullable=False))
        batch_op.add_column(sa.Column('seeking_description', sa.String(length=1000), nullable=True))
        batch_op.add_column(sa.Column('website_link', sa.String(length=120), nullable=True))
        batch_op.add_column(sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True))

    with op.batch_alter_table('Venue', schema=None) as batch_op:
        batch_op.add_column(sa.Column('seeking_talent', sa.Boolean(), nullable=False))
        batch_op.add_column(sa.Column('seeking_description', sa.String(length=1000), nullable=True))
        batch_op.add_column(sa.Column('website_link', sa.String(length=120), nullable=True))
        batch_op.add_column(sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Venue', schema=None) as batch_op:
        batch_op.drop_column('created_at')
        batch_op.drop_column('website_link')
        batch_op.drop_column('seeking_description')
        batch_op.drop_column('seeking_talent')

    with op.batch_alter_table('Artist', schema=None) as batch_op:
        batch_op.drop_column('created_at')
        batch_op.drop_column('website_link')
        batch_op.drop_column('seeking_description')
        batch_op.drop_column('seeking_venue')

    op.drop_table('Show')
    # ### end Alembic commands ###
