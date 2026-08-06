from alembic import op
import sqlalchemy as sa


revision = "001_add_hospital_isolation"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ===============================
    # CREATE HOSPITALS TABLE
    # ===============================
    op.create_table(
        "hospitals",
        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True
        ),
        sa.Column(
            "name",
            sa.String(length=150),
            nullable=False
        ),
        sa.Column(
            "active",
            sa.Boolean(),
            server_default=sa.text("true")
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now()
        )
    )

    # ===============================
    # DEFAULT HOSPITAL
    # ===============================
    op.execute(
        """
        INSERT INTO hospitals
        (id,name,active)
        VALUES
        (1,'METHYLOX Default Hospital',true)
        """
    )

    # ===============================
    # ADD HOSPITAL COLUMNS
    # ===============================
    op.add_column(
        "users",
        sa.Column(
            "hospital_id",
            sa.Integer(),
            nullable=True
        )
    )

    op.add_column(
        "patients",
        sa.Column(
            "hospital_id",
            sa.Integer(),
            nullable=True
        )
    )

    op.add_column(
        "samples",
        sa.Column(
            "hospital_id",
            sa.Integer(),
            nullable=True
        )
    )

    # ===============================
    # FOREIGN KEYS
    # ===============================
    op.create_foreign_key(
        "fk_users_hospital",
        "users",
        "hospitals",
        ["hospital_id"],
        ["id"]
    )

    op.create_foreign_key(
        "fk_patients_hospital",
        "patients",
        "hospitals",
        ["hospital_id"],
        ["id"]
    )

    op.create_foreign_key(
        "fk_samples_hospital",
        "samples",
        "hospitals",
        ["hospital_id"],
        ["id"]
    )

    # ===============================
    # UPDATE EXISTING DATA
    # ===============================
    op.execute(
        """
        UPDATE users
        SET hospital_id = 1
        WHERE hospital_id IS NULL
        """
    )

    op.execute(
        """
        UPDATE patients
        SET hospital_id = 1
        WHERE hospital_id IS NULL
        """
    )

    op.execute(
        """
        UPDATE samples
        SET hospital_id = 1
        WHERE hospital_id IS NULL
        """
    )


def downgrade():
    op.drop_constraint(
        "fk_samples_hospital",
        "samples",
        type_="foreignkey"
    )

    op.drop_constraint(
        "fk_patients_hospital",
        "patients",
        type_="foreignkey"
    )

    op.drop_constraint(
        "fk_users_hospital",
        "users",
        type_="foreignkey"
    )

    op.drop_column(
        "samples",
        "hospital_id"
    )

    op.drop_column(
        "patients",
        "hospital_id"
    )

    op.drop_column(
        "users",
        "hospital_id"
    )

    op.drop_table(
        "hospitals"
    )
