"""add hospital_id to audit_logs

Revision ID: add_hospital_id_audit
Revises: 
Create Date: 2026-08-08
"""

from alembic import op
import sqlalchemy as sa

revision = "add_hospital_id_audit"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.add_column("audit_logs", sa.Column("hospital_id", sa.Integer(), nullable=True))
    op.create_foreign_key("fk_audit_logs_hospital_id", "audit_logs", "hospitals", ["hospital_id"], ["id"])

def downgrade():
    op.drop_constraint("fk_audit_logs_hospital_id", "audit_logs", type_="foreignkey")
    op.drop_column("audit_logs", "hospital_id")
