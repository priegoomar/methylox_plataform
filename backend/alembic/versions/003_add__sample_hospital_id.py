from alembic import op
import sqlalchemy as sa


revision = "003_add_sample_hospital_id"
down_revision = "002_add_patient_hospital_column"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "samples",
        sa.Column(
            "hospital_id",
            sa.Integer(),
            nullable=True
        )
    )

    op.create_foreign_key(
        "fk_samples_hospital",
        "samples",
        "hospitals",
        ["hospital_id"],
        ["id"]
    )

    op.execute(
        """
        UPDATE samples
        SET hospital_id = (
            SELECT hospital_id
            FROM patients
            WHERE patients.id = samples.patient_id
        )
        """
    )


def downgrade():
    op.drop_constraint(
        "fk_samples_hospital",
        "samples",
        type_="foreignkey"
    )

    op.drop_column(
        "samples",
        "hospital_id"
    )
