from alembic import op
import sqlalchemy as sa

# ============================================================
# MIGRATION IDENTIFICATION
# ============================================================

revision = "005_add_audit_trail"
down_revision = "004_add_analysis_hospital_id"
branch_labels = None
depends_on = None

# ============================================================
# UPGRADE
# ============================================================

def upgrade():
    # IP address of the client
    op.add_column("audit_logs", sa.Column("ip_address", sa.String(45), nullable=True))

    # API endpoint used
    op.add_column("audit_logs", sa.Column("endpoint", sa.String(255), nullable=True))

    # HTTP method used
    op.add_column("audit_logs", sa.Column("http_method", sa.String(10), nullable=True))

    # HTTP response status code
    op.add_column("audit_logs", sa.Column("status_code", sa.Integer(), nullable=True))

# ============================================================
# DOWNGRADE
# ============================================================

def downgrade():
    op.drop_column("audit_logs", "status_code")
    op.drop_column("audit_logs", "http_method")
    op.drop_column("audit_logs", "endpoint")
    op.drop_column("audit_logs", "ip_address")
