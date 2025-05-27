"""Initial migration

Revision ID: 001
Revises: 
Create Date: 2024-01-15 10:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Create users table
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('email', sa.String(length=100), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('full_name', sa.String(length=100), nullable=True),
        sa.Column('role', sa.Enum('ADMIN', 'USER', 'VIEWER', name='userrole'), nullable=True),
        sa.Column('is_verified', sa.Boolean(), nullable=True),
        sa.Column('avatar_url', sa.String(length=255), nullable=True),
        sa.Column('business_name', sa.String(length=100), nullable=True),
        sa.Column('default_markup_percentage', sa.Float(), nullable=True),
        sa.Column('currency', sa.String(length=3), nullable=True),
        sa.Column('timezone', sa.String(length=50), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)

    # Create projects table
    op.create_table('projects',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('client_name', sa.String(length=100), nullable=True),
        sa.Column('client_email', sa.String(length=100), nullable=True),
        sa.Column('platform', sa.Enum('THINGIVERSE', 'MYMINIFACTORY', 'CULTS3D', 'PATREON', 'DIRECT', name='marketplaceplatform'), nullable=True),
        sa.Column('status', sa.Enum('PLANNING', 'IN_PROGRESS', 'ON_HOLD', 'COMPLETED', 'CANCELLED', name='projectstatus'), nullable=True),
        sa.Column('due_date', sa.DateTime(), nullable=True),
        sa.Column('budget', sa.Float(), nullable=True),
        sa.Column('estimated_hours', sa.Float(), nullable=True),
        sa.Column('actual_hours', sa.Float(), nullable=True),
        sa.Column('estimated_cost', sa.Float(), nullable=True),
        sa.Column('actual_cost', sa.Float(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_projects_id'), 'projects', ['id'], unique=False)

    # Create materials table
    op.create_table('materials',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('brand', sa.String(length=50), nullable=True),
        sa.Column('material_type', sa.Enum('FILAMENT', 'RESIN', 'POWDER', 'OTHER', name='materialtype'), nullable=True),
        sa.Column('color', sa.String(length=30), nullable=True),
        sa.Column('current_stock', sa.Float(), nullable=True),
        sa.Column('unit', sa.String(length=10), nullable=True),
        sa.Column('low_stock_threshold', sa.Float(), nullable=True),
        sa.Column('reorder_threshold', sa.Float(), nullable=True),
        sa.Column('cost_per_unit', sa.Float(), nullable=False),
        sa.Column('supplier', sa.String(length=100), nullable=True),
        sa.Column('supplier_sku', sa.String(length=50), nullable=True),
        sa.Column('properties', sa.JSON(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_materials_id'), 'materials', ['id'], unique=False)

    # Create quotes table
    op.create_table('quotes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('quote_number', sa.String(length=50), nullable=True),
        sa.Column('client_name', sa.String(length=100), nullable=False),
        sa.Column('client_email', sa.String(length=100), nullable=True),
        sa.Column('client_phone', sa.String(length=20), nullable=True),
        sa.Column('subtotal', sa.Float(), nullable=True),
        sa.Column('markup_percentage', sa.Float(), nullable=True),
        sa.Column('markup_amount', sa.Float(), nullable=True),
        sa.Column('total_amount', sa.Float(), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=True),
        sa.Column('valid_until', sa.DateTime(), nullable=True),
        sa.Column('sent_date', sa.DateTime(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('terms_conditions', sa.Text(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_quotes_id'), 'quotes', ['id'], unique=False)
    op.create_index(op.f('ix_quotes_quote_number'), 'quotes', ['quote_number'], unique=True)

    # Create model_files table
    op.create_table('model_files',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('filename', sa.String(length=255), nullable=False),
        sa.Column('original_filename', sa.String(length=255), nullable=True),
        sa.Column('file_path', sa.String(length=500), nullable=True),
        sa.Column('file_size', sa.Integer(), nullable=True),
        sa.Column('file_type', sa.String(length=10), nullable=True),
        sa.Column('title', sa.String(length=200), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('tags', sa.JSON(), nullable=True),
        sa.Column('estimated_print_time', sa.Float(), nullable=True),
        sa.Column('estimated_material_usage', sa.Float(), nullable=True),
        sa.Column('support_required', sa.Boolean(), nullable=True),
        sa.Column('seo_title', sa.String(length=200), nullable=True),
        sa.Column('seo_description', sa.Text(), nullable=True),
        sa.Column('marketplace_urls', sa.JSON(), nullable=True),
        sa.Column('project_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_model_files_id'), 'model_files', ['id'], unique=False)

    # Create quote_items table
    op.create_table('quote_items',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('description', sa.String(length=500), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=True),
        sa.Column('unit_price', sa.Float(), nullable=False),
        sa.Column('total_price', sa.Float(), nullable=True),
        sa.Column('print_time_hours', sa.Float(), nullable=True),
        sa.Column('material_usage', sa.Float(), nullable=True),
        sa.Column('material_cost', sa.Float(), nullable=True),
        sa.Column('quote_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['quote_id'], ['quotes.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_quote_items_id'), 'quote_items', ['id'], unique=False)

    # Create project_costs table
    op.create_table('project_costs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('category', sa.String(length=50), nullable=False),
        sa.Column('item_name', sa.String(length=100), nullable=False),
        sa.Column('quantity', sa.Float(), nullable=True),
        sa.Column('unit_cost', sa.Float(), nullable=False),
        sa.Column('total_cost', sa.Float(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('project_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_project_costs_id'), 'project_costs', ['id'], unique=False)

    # Create inventory_transactions table
    op.create_table('inventory_transactions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('transaction_type', sa.String(length=20), nullable=False),
        sa.Column('quantity', sa.Float(), nullable=False),
        sa.Column('unit_cost', sa.Float(), nullable=True),
        sa.Column('reference', sa.String(length=100), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('material_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['material_id'], ['materials.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_inventory_transactions_id'), 'inventory_transactions', ['id'], unique=False)

    # Create marketplace_accounts table
    op.create_table('marketplace_accounts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('platform', sa.Enum('THINGIVERSE', 'MYMINIFACTORY', 'CULTS3D', 'PATREON', 'DIRECT', name='marketplaceplatform'), nullable=False),
        sa.Column('username', sa.String(length=100), nullable=True),
        sa.Column('api_key', sa.String(length=255), nullable=True),
        sa.Column('api_secret', sa.String(length=255), nullable=True),
        sa.Column('is_connected', sa.Boolean(), nullable=True),
        sa.Column('last_sync', sa.DateTime(), nullable=True),
        sa.Column('total_views', sa.Integer(), nullable=True),
        sa.Column('total_downloads', sa.Integer(), nullable=True),
        sa.Column('total_revenue', sa.Float(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_marketplace_accounts_id'), 'marketplace_accounts', ['id'], unique=False)

    # Create user_settings table
    op.create_table('user_settings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('setting_key', sa.String(length=100), nullable=False),
        sa.Column('setting_value', sa.JSON(), nullable=True),
        sa.Column('setting_type', sa.String(length=20), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_settings_id'), 'user_settings', ['id'], unique=False)

def downgrade() -> None:
    # Drop all tables in reverse order
    op.drop_index(op.f('ix_user_settings_id'), table_name='user_settings')
    op.drop_table('user_settings')
    
    op.drop_index(op.f('ix_marketplace_accounts_id'), table_name='marketplace_accounts')
    op.drop_table('marketplace_accounts')
    
    op.drop_index(op.f('ix_inventory_transactions_id'), table_name='inventory_transactions')
    op.drop_table('inventory_transactions')
    
    op.drop_index(op.f('ix_project_costs_id'), table_name='project_costs')
    op.drop_table('project_costs')
    
    op.drop_index(op.f('ix_quote_items_id'), table_name='quote_items')
    op.drop_table('quote_items')
    
    op.drop_index(op.f('ix_model_files_id'), table_name='model_files')
    op.drop_table('model_files')
    
    op.drop_index(op.f('ix_quotes_quote_number'), table_name='quotes')
    op.drop_index(op.f('ix_quotes_id'), table_name='quotes')
    op.drop_table('quotes')
    
    op.drop_index(op.f('ix_materials_id'), table_name='materials')
    op.drop_table('materials')
    
    op.drop_index(op.f('ix_projects_id'), table_name='projects')
    op.drop_table('projects')
    
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    
    # Drop enums
    op.execute('DROP TYPE IF EXISTS userrole CASCADE')
    op.execute('DROP TYPE IF EXISTS marketplaceplatform CASCADE')
    op.execute('DROP TYPE IF EXISTS projectstatus CASCADE')
    op.execute('DROP TYPE IF EXISTS materialtype CASCADE')