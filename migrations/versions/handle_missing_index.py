from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector

revision = 'handle_missing_index'
down_revision = None  # Replace with the previous migration's revision id
branch_labels = None
depends_on = None

def upgrade():
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    indexes = inspector.get_indexes('village')
    if any(index['name'] == 'ix_village_name' for index in indexes):
        op.drop_index('ix_village_name', table_name='village')
    else:
        print("Index 'ix_village_name' does not exist, skipping drop operation")

def downgrade():
    # Add downgrade operations if needed
    pass
