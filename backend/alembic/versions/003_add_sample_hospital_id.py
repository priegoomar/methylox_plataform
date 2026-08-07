from alembic import op
import sqlalchemy as sa


revision = "003_add_sample_hospital_id"
down_revision = "002_add_patient_hospital_column"
branch_labels = None
depends_on = None


def upgrade():
    # Crear hospital por defecto si no existe
    op.execute(
        """
        INSERT INTO hospitals (id, name, active)
        VALUES (1, 'Hospital Universitario', true)
        ON CONFLICT (id) DO NOTHING;
        """
    )

    # Crear columna si no existe
    op.add_column(
        "samples",
        sa.Column(
            "hospital_id",
            sa.Integer(),
            nullable=True
        )
    )

    # Crear relación
    op.create_foreign_key(
        "fk_samples_hospital",
        "samples",
        "hospitals",
        ["hospital_id"],
        ["id"]
    )

    # Copiar hospital desde pacientes
    op.execute(
        """
        UPDATE samples
        SET hospital_id = patients.hospital_id
        FROM patients
        WHERE samples.patient_id = patients.id;
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
