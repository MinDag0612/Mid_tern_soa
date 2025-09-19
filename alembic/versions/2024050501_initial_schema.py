"""Initial schema for tuition payment system"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "2024050501"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "account",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("userName", sa.String(length=50), nullable=False),
        sa.Column("password", sa.String(length=255), nullable=False),
        sa.UniqueConstraint("userName", name="uq_account_username"),
        mysql_engine="InnoDB",
        mysql_charset="utf8mb4",
        mysql_collate="utf8mb4_unicode_ci",
    )

    op.create_table(
        "CustomerInfor",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("fullName", sa.String(length=50), nullable=False),
        sa.Column("phoneNumber", sa.String(length=20), nullable=True),
        sa.Column("email", sa.String(length=50), nullable=True),
        sa.Column(
            "balance",
            sa.Numeric(precision=15, scale=2),
            nullable=False,
            server_default=sa.text("0"),
        ),
        sa.ForeignKeyConstraint(
            ["id"],
            ["account.id"],
            name="fk_customerinfo_account",
            ondelete="CASCADE",
        ),
        sa.UniqueConstraint("phoneNumber", name="uq_customerinfo_phone"),
        sa.UniqueConstraint("email", name="uq_customerinfo_email"),
        mysql_engine="InnoDB",
        mysql_charset="utf8mb4",
        mysql_collate="utf8mb4_unicode_ci",
    )

    op.create_table(
        "tuition",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("idTransaction", sa.String(length=20), nullable=False),
        sa.Column("studentId", sa.String(length=20), nullable=False),
        sa.Column("studentName", sa.String(length=50), nullable=False),
        sa.Column(
            "tuition",
            sa.Numeric(precision=15, scale=2),
            nullable=False,
        ),
        sa.Column(
            "is_paid",
            sa.Boolean(create_constraint=False),
            nullable=False,
            server_default=sa.text("0"),
        ),
        sa.Column("paid_at", sa.DateTime(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.UniqueConstraint("idTransaction", name="uq_tuition_transaction_code"),
        mysql_engine="InnoDB",
        mysql_charset="utf8mb4",
        mysql_collate="utf8mb4_unicode_ci",
    )

    op.create_table(
        "history",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("idTransaction", sa.String(length=20), nullable=False),
        sa.Column("studentId", sa.String(length=20), nullable=False),
        sa.Column(
            "tuition",
            sa.Numeric(precision=15, scale=2),
            nullable=False,
        ),
        sa.Column("dayComplete", sa.DateTime(), nullable=False),
        sa.Column("payer", sa.String(length=50), nullable=False),
        sa.Column("email", sa.String(length=50), nullable=True),
        sa.Column(
            "status",
            sa.String(length=20),
            nullable=False,
            server_default=sa.text("'SUCCESS'"),
        ),
        sa.Column("customer_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["idTransaction"],
            ["tuition.idTransaction"],
            name="fk_history_tuition",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["customer_id"],
            ["CustomerInfor.id"],
            name="fk_history_customer",
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["email"],
            ["CustomerInfor.email"],
            name="fk_history_customer_email",
            ondelete="SET NULL",
        ),
        sa.UniqueConstraint("idTransaction", name="uq_history_transaction"),
        mysql_engine="InnoDB",
        mysql_charset="utf8mb4",
        mysql_collate="utf8mb4_unicode_ci",
    )

    op.create_table(
        "payment_otp",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("idTransaction", sa.String(length=20), nullable=False),
        sa.Column("otp_code", sa.String(length=10), nullable=False),
        sa.Column("expires_at", sa.DateTime(), nullable=False),
        sa.Column("verified_at", sa.DateTime(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.ForeignKeyConstraint(
            ["idTransaction"],
            ["tuition.idTransaction"],
            name="fk_payment_otp_tuition",
            ondelete="CASCADE",
        ),
        mysql_engine="InnoDB",
        mysql_charset="utf8mb4",
        mysql_collate="utf8mb4_unicode_ci",
    )
    op.create_index(
        "ix_payment_otp_transaction",
        "payment_otp",
        ["idTransaction"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_payment_otp_transaction", table_name="payment_otp")
    op.drop_table("payment_otp")
    op.drop_table("history")
    op.drop_table("tuition")
    op.drop_table("CustomerInfor")
    op.drop_table("account")
