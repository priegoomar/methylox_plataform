from alembic import op
import sqlalchemy as sa

revision = "001_add_hospital_isolation"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        "hospitals",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("active", sa.Boolean(), server_default="true"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now()
        )
    )

    op.execute("""
        INSERT INTO hospitals (id, name, active)
        VALUES (1, 'METHYLOX Default Hospital', true)
    """)

    op.add_column(
        "patients",
        sa.Column(
            "hospital_id",
            sa.Integer(),
            nullable=True
        )
    )

    op.create_foreign_key(
        "fk_patients_hospital",
        "patients",
        "hospitals",
        ["hospital_id"],
        ["id"]
    )

    op.execute(
        "UPDATE patients SET hospital_id = 1 WHERE hospital_id IS NULL"
    )

def downgrade():
    op.drop_constraint(
        "fk_patients_hospital",
        "patients",
        type_="foreignkey"
    )

    op.drop_column(
        "patients",
        "hospital_id"
    )

    op.drop_table("hospitals")
