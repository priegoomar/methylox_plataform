from alembic import op
import sqlalchemy as sa


# ============================================================
# MIGRATION 005
# ADD HOSPITAL ID TO AUDIT LOGS
# ============================================================

revision = "005_add_hospital_id_to_audit_logs"
down_revision = "004_add_analysis_hospital_id"
branch_labels = None
depends_on = None


def upgrade():
    # --------------------------------------------------------
    # Add hospital_id column
    # --------------------------------------------------------
    op.add_column("audit_logs", sa.Column("hospital_id", sa.Integer(), nullable=True))

    # --------------------------------------------------------
    # Create foreign key
    # --------------------------------------------------------
    op.create_foreign_key(
        "fk_audit_logs_hospital",
        "audit_logs",
        "hospitals",
        ["hospital_id"],
        ["id"]
    )

    # --------------------------------------------------------
    # Populate existing audit records
    # using the hospital of the user who created the log
    # --------------------------------------------------------
    op.execute(
        """
        UPDATE audit_logs
        SET hospital_id = users.hospital_id
        FROM users
        WHERE audit_logs.user_id = users.id
        """
    )


def downgrade():
    # --------------------------------------------------------
    # Remove foreign key
    # --------------------------------------------------------
    op.drop_constraint(
        "fk_audit_logs_hospital",
        "audit_logs",
        type_="foreignkey"
    )

    # --------------------------------------------------------
    # Remove hospital_id
    # --------------------------------------------------------
    op.drop_column("audit_logs", "hospital_id")
