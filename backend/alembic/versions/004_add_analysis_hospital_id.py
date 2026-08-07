from alembic import op
import sqlalchemy as sa


revision = "004_add_analysis_hospital_id"
down_revision = "003_add_sample_hospital_id"
branch_labels = None
depends_on = None


def upgrade():

    op.add_column(
        "analysis_results",
        sa.Column(
            "hospital_id",
            sa.Integer(),
            nullable=True
        )
    )


    op.create_foreign_key(
        "fk_analysis_results_hospital",
        "analysis_results",
        "hospitals",
        ["hospital_id"],
        ["id"]
    )


    op.execute(
        """
        UPDATE analysis_results
        SET hospital_id = (
            SELECT samples.hospital_id
            FROM samples
            WHERE samples.id = analysis_results.sample_id
        )
        """
    )


def downgrade():

    op.drop_constraint(
        "fk_analysis_results_hospital",
        "analysis_results",
        type_="foreignkey"
    )


    op.drop_column(
        "analysis_results",
        "hospital_id"
    )
