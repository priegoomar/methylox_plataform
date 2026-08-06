from alembic import op
import sqlalchemy as sa


revision = "002_add_patient_hospital_id"
down_revision = "001_add_hospital_isolation"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "patients",
        sa.Column(
            "hospital_id",
            sa.Integer(),
            nullable=True
        )
    )


def downgrade():
    op.drop_column(
        "patients",
        "hospital_id"
    )
