from __future__ import annotations

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "2024050503"
down_revision = "2024050502"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "payment_otp",
        sa.Column("requested_by", sa.Integer(), nullable=True),
    )
    op.add_column(
        "payment_otp",
        sa.Column(
            "requested_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
    )
    op.create_index(
        "ix_payment_otp_requested_by",
        "payment_otp",
        ["requested_by"],
        unique=False,
    )

    op.create_table(
        "otp_audit",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("idTransaction", sa.String(length=20), nullable=False),
        sa.Column("customer_id", sa.Integer(), nullable=True),
        sa.Column("email", sa.String(length=50), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("detail", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.ForeignKeyConstraint(
            ["idTransaction"],
            ["tuition.idTransaction"],
            name="fk_otp_audit_tuition",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["customer_id"],
            ["CustomerInfor.id"],
            name="fk_otp_audit_customer",
            ondelete="SET NULL",
        ),
    )
    op.create_index(
        "ix_otp_audit_transaction",
        "otp_audit",
        ["idTransaction"],
        unique=False,
    )

    op.execute(
        "ALTER TABLE payment_otp MODIFY requested_at DATETIME NOT NULL"
    )


def downgrade() -> None:
    op.drop_index("ix_otp_audit_transaction", table_name="otp_audit")
    op.drop_table("otp_audit")

    op.drop_index("ix_payment_otp_requested_by", table_name="payment_otp")
    op.drop_column("payment_otp", "requested_at")
    op.drop_column("payment_otp", "requested_by")
