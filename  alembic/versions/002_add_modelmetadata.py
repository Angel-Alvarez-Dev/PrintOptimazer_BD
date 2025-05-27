"""add model_metadata table

Revision ID: 002_add_modelmetadata
Revises: 001_initial_migration
Create Date: 2025-05-27 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '002_add_modelmetadata'
down_revision = '001_initial_migration'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'model_metadata',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('model_id', sa.String(length=36), nullable=False, index=True),
        sa.Column('seo_title', sa.String(length=100), nullable=True),
        sa.Column('market_description', sa.Text, nullable=True),
        sa.Column('tags', sa.JSON, nullable=True),
        sa.Column('vertices', sa.Integer, nullable=True),
        sa.Column('polygons', sa.Integer, nullable=True),
        sa.Column('file_size_kb', sa.Float, nullable=True),
        sa.Column('complexity_score', sa.Float, nullable=True),
        sa.Column('estimated_time_minutes', sa.Float, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )


def downgrade():
    op.drop_table('model_metadata')