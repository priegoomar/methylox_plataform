from alembic import op
import sqlalchemy as sa


# ============================================================
# MIGRATION 005
# COMPLETE AUDIT TRAIL
# ============================================================

revision = "005_add_audit_trail"
down_revision = "004_add_analysis_hospital_id"
branch_labels = None
depends_on = None


# ============================================================
# UPGRADE
# ============================================================

def upgrade():
    # --------------------------------------------------------
    # Hospital associated with the audit event
    # --------------------------------------------------------
    op.add_column("audit_logs", sa.Column("hospital_id", sa.Integer(), nullable=True))

    op.create_foreign_key(
        "fk_audit_logs_hospital",
        "audit_logs",
        "hospitals",
        ["hospital_id"],
        ["id"]
    )

    # --------------------------------------------------------
    # IP address
    # --------------------------------------------------------
    op.add_column("audit_logs", sa.Column("ip_address", sa.String(45), nullable=True))

    # --------------------------------------------------------
    # API endpoint
    # --------------------------------------------------------
    op.add_column("audit_logs", sa.Column("endpoint", sa.String(255), nullable=True))

    # --------------------------------------------------------
    # HTTP method
    # --------------------------------------------------------
    op.add_column("audit_logs", sa.Column("http_method", sa.String(10), nullable=True))

    # --------------------------------------------------------
    # HTTP status code
    # --------------------------------------------------------
    op.add_column("audit_logs", sa.Column("status_code", sa.Integer(), nullable=True))

    # --------------------------------------------------------
    # Populate hospital_id for existing audit records
    # using the hospital of the user who created the event
    # --------------------------------------------------------
    op.execute(
        """
        UPDATE audit_logs
        SET hospital_id = users.hospital_id
        FROM users
        WHERE audit_logs.user_id = users.id
        """
    )


# ============================================================
# DOWNGRADE
# ============================================================

def downgrade():
    op.drop_constraint(
        "fk_audit_logs_hospital",
        "audit_logs",
        type_="foreignkey"
    )

    op.drop_column("audit_logs", "status_code")
    op.drop_column("audit_logs", "http_method")
    op.drop_column("audit_logs", "endpoint")
    op.drop_column("audit_logs", "ip_address")
    op.drop_column("audit_logs", "hospital_id")
