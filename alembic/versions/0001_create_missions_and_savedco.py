"""create missions table and add saved_co to user

Revision ID: 0001_create_missions_and_savedco
Revises: 
Create Date: 2025-12-05 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001_create_missions_and_savedco'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create mission table if not exists
    op.create_table(
        'mission',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('co2_reduction', sa.Integer(), nullable=True),
    )
    # Add saved_co to user if not exists (SQLite simple check)
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    cols = [c['name'] for c in inspector.get_columns('user')] if 'user' in inspector.get_table_names() else []
    if 'saved_co' not in cols:
        op.add_column('user', sa.Column('saved_co', sa.Integer(), server_default='0'))


def downgrade():
    # downgrade: remove column and table (be careful with data loss)
    try:
        op.drop_table('mission')
    except Exception:
        pass
    # Removing column in sqlite is not trivial; leave it for manual rollback
    pass
