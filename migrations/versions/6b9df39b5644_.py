"""empty message

Revision ID: 6b9df39b5644
Revises: 
Create Date: 2017-06-05 12:35:28.223883

"""
from alembic import op, context
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from flask import current_app

# revision identifiers, used by Alembic.
revision = '6b9df39b5644'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('title',
    sa.Column('title_id', postgresql.UUID(), nullable=False),
    sa.Column('foo', sa.String(), nullable=False),
    sa.Column('bar', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('archived_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('title_id')
    )
    # ### end Alembic commands ###

    # ### Grant permissions for the user found in config variable APP_SQL_USERNAME ###
    context.execute("GRANT SELECT, UPDATE, INSERT, DELETE ON TABLE title TO " + current_app.config.get('APP_SQL_USERNAME'))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('title')
    # ### end Alembic commands ###