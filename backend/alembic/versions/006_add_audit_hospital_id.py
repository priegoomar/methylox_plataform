from alembic import op
import sqlalchemy as sa

# ============================================================
# MIGRATION IDENTIFICATION
# ============================================================

revision = "006_add_audit_hospital_id"
down_revision = "005_add_audit_trail"
branch_labels = None
depends_on = None

# ============================================================
# UPGRADE
# ============================================================

def upgrade():
    # --------------------------------------------------------
    # Add hospital_id to audit_logs
    # --------------------------------------------------------
    op.add_column("audit_logs", sa.Column("hospital_id", sa.Integer(), nullable=True))

    # --------------------------------------------------------
    # Foreign key to hospitals
    # --------------------------------------------------------
    op.create_foreign_key(
        "fk_audit_logs_hospital",
        "audit_logs",
        "hospitals",
        ["hospital_id"],
        ["id"]
    )

    # --------------------------------------------------------
    # Populate existing audit records using the user hospital
    # --------------------------------------------------------
    op.execute(
        """
        UPDATE audit_logs
        SET hospital_id = users.hospital_id
        FROM users
        WHERE audit_logs.user_id = users.id
          AND audit_logs.hospital_id IS NULL
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
    op.drop_column("audit_logs", "hospital_id")
