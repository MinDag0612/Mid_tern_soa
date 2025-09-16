"""Seed initial data for tuition payment system"""

from __future__ import annotations

from datetime import datetime

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "2024050502"
down_revision = "2024050501"
branch_labels = None
depends_on = None


ACCOUNT_DATA = [
    {
        "id": 1,
        "userName": "admin",
        "password": "$2b$12$ByWI/aiBcz5.ojnuAKJ.ueuwT1MPL2X5vd5Klx5yDsRkk0.PoX1dS",
    },
    {
        "id": 2,
        "userName": "student01",
        "password": "$2b$12$J0/ryTNcS0btK0uRkTj0f.zASkMVRWRnxytSQ01BGBqoxz.M3aTDq",
    },
    {
        "id": 3,
        "userName": "student02",
        "password": "$2b$12$CQaG1mDCWWwMJ2bAS1gBBub8wA8G1ARqlMRy2oGcuWQzypI6JapBG",
    },
]

CUSTOMER_DATA = [
    {
        "id": 1,
        "fullName": "Nguyen Van A",
        "phoneNumber": "0901234567",
        "email": "a@example.com",
        "balance": 5000000,
    },
    {
        "id": 2,
        "fullName": "Tran Thi B",
        "phoneNumber": "0912345678",
        "email": "b@example.com",
        "balance": 3000000,
    },
    {
        "id": 3,
        "fullName": "Le Van C",
        "phoneNumber": "0923456789",
        "email": "c@example.com",
        "balance": 4500000,
    },
]

TUITION_DATA = [
    {
        "id": 1,
        "idTransaction": "TXN001",
        "studentId": "ST001",
        "studentName": "Nguyen Van A",
        "tuition": 1500000,
        "is_paid": True,
        "paid_at": datetime.utcnow(),
    },
    {
        "id": 2,
        "idTransaction": "TXN002",
        "studentId": "ST002",
        "studentName": "Tran Thi B",
        "tuition": 2000000,
        "is_paid": True,
        "paid_at": datetime.utcnow(),
    },
    {
        "id": 3,
        "idTransaction": "TXN003",
        "studentId": "ST003",
        "studentName": "Le Van C",
        "tuition": 1800000,
        "is_paid": False,
        "paid_at": None,
    },
]

HISTORY_DATA = [
    {
        "id": 1,
        "idTransaction": "TXN001",
        "studentId": "ST001",
        "tuition": 1500000,
        "dayComplete": datetime.utcnow(),
        "payer": "Nguyen Van A",
        "email": "a@example.com",
        "status": "SUCCESS",
        "customer_id": 1,
    },
    {
        "id": 2,
        "idTransaction": "TXN002",
        "studentId": "ST002",
        "tuition": 2000000,
        "dayComplete": datetime.utcnow(),
        "payer": "Tran Thi B",
        "email": "b@example.com",
        "status": "SUCCESS",
        "customer_id": 2,
    },
]


def upgrade() -> None:
    account_table = sa.table(
        "account",
        sa.column("id", sa.Integer()),
        sa.column("userName", sa.String(length=50)),
        sa.column("password", sa.String(length=255)),
    )
    customer_table = sa.table(
        "CustomerInfor",
        sa.column("id", sa.Integer()),
        sa.column("fullName", sa.String(length=50)),
        sa.column("phoneNumber", sa.String(length=20)),
        sa.column("email", sa.String(length=50)),
        sa.column("balance", sa.Numeric(precision=15, scale=2)),
    )
    tuition_table = sa.table(
        "tuition",
        sa.column("id", sa.Integer()),
        sa.column("idTransaction", sa.String(length=20)),
        sa.column("studentId", sa.String(length=20)),
        sa.column("studentName", sa.String(length=50)),
        sa.column("tuition", sa.Numeric(precision=15, scale=2)),
        sa.column("is_paid", sa.Boolean()),
        sa.column("paid_at", sa.DateTime()),
    )
    history_table = sa.table(
        "history",
        sa.column("id", sa.Integer()),
        sa.column("idTransaction", sa.String(length=20)),
        sa.column("studentId", sa.String(length=20)),
        sa.column("tuition", sa.Numeric(precision=15, scale=2)),
        sa.column("dayComplete", sa.DateTime()),
        sa.column("payer", sa.String(length=50)),
        sa.column("email", sa.String(length=50)),
        sa.column("status", sa.String(length=20)),
        sa.column("customer_id", sa.Integer()),
    )

    op.bulk_insert(account_table, ACCOUNT_DATA)
    op.bulk_insert(customer_table, CUSTOMER_DATA)
    op.bulk_insert(tuition_table, TUITION_DATA)
    op.bulk_insert(history_table, HISTORY_DATA)


def downgrade() -> None:
    op.execute("DELETE FROM history")
    op.execute("DELETE FROM tuition")
    op.execute("DELETE FROM CustomerInfor")
    op.execute("DELETE FROM account")
