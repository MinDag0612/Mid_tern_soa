"""Add additional sample data for testing."""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision = "2024050504"
down_revision = "2024050503"
branch_labels = None
depends_on = None


ACCOUNT_TABLE = sa.table(
    "account",
    sa.column("id", sa.Integer()),
    sa.column("userName", sa.String(length=50)),
    sa.column("password", sa.String(length=255)),
)

CUSTOMER_TABLE = sa.table(
    "CustomerInfor",
    sa.column("id", sa.Integer()),
    sa.column("fullName", sa.String(length=50)),
    sa.column("phoneNumber", sa.String(length=20)),
    sa.column("email", sa.String(length=50)),
    sa.column("balance", sa.Numeric(15, 2)),
)

TUITION_TABLE = sa.table(
    "tuition",
    sa.column("id", sa.Integer()),
    sa.column("idTransaction", sa.String(length=20)),
    sa.column("studentId", sa.String(length=20)),
    sa.column("studentName", sa.String(length=50)),
    sa.column("tuition", sa.Numeric(15, 2)),
    sa.column("is_paid", sa.Boolean()),
    sa.column("paid_at", sa.DateTime()),
)

HISTORY_TABLE = sa.table(
    "history",
    sa.column("id", sa.Integer()),
    sa.column("idTransaction", sa.String(length=20)),
    sa.column("studentId", sa.String(length=20)),
    sa.column("tuition", sa.Numeric(15, 2)),
    sa.column("dayComplete", sa.DateTime()),
    sa.column("payer", sa.String(length=50)),
    sa.column("email", sa.String(length=50)),
    sa.column("status", sa.String(length=20)),
)


def upgrade() -> None:
    op.bulk_insert(
        ACCOUNT_TABLE,
        [
            {"id": 4, "userName": "student03", "password": "$2b$12$CQaG1mDCWWwMJ2bAS1gBBub8wA8G1ARqlMRy2oGcuWQzypI6JapBG"},
            {"id": 5, "userName": "student04", "password": "$2b$12$CQaG1mDCWWwMJ2bAS1gBBub8wA8G1ARqlMRy2oGcuWQzypI6JapBG"},
            {"id": 6, "userName": "student05", "password": "$2b$12$CQaG1mDCWWwMJ2bAS1gBBub8wA8G1ARqlMRy2oGcuWQzypI6JapBG"},
            {"id": 7, "userName": "student06", "password": "$2b$12$CQaG1mDCWWwMJ2bAS1gBBub8wA8G1ARqlMRy2oGcuWQzypI6JapBG"},
            {"id": 8, "userName": "student07", "password": "$2b$12$CQaG1mDCWWwMJ2bAS1gBBub8wA8G1ARqlMRy2oGcuWQzypI6JapBG"},
            {"id": 9, "userName": "student08", "password": "$2b$12$CQaG1mDCWWwMJ2bAS1gBBub8wA8G1ARqlMRy2oGcuWQzypI6JapBG"},
            {"id": 10, "userName": "student09", "password": "$2b$12$CQaG1mDCWWwMJ2bAS1gBBub8wA8G1ARqlMRy2oGcuWQzypI6JapBG"},
            {"id": 11, "userName": "student10", "password": "$2b$12$CQaG1mDCWWwMJ2bAS1gBBub8wA8G1ARqlMRy2oGcuWQzypI6JapBG"},
        ],
    )

    op.bulk_insert(
        CUSTOMER_TABLE,
        [
            {"id": 4, "fullName": "Pham Thi D", "phoneNumber": "0901111114", "email": "d@example.com", "balance": 4200000},
            {"id": 5, "fullName": "Hoang Van E", "phoneNumber": "0901111115", "email": "e@example.com", "balance": 3800000},
            {"id": 6, "fullName": "Le Thi F", "phoneNumber": "0901111116", "email": "f@example.com", "balance": 2500000},
            {"id": 7, "fullName": "Do Van G", "phoneNumber": "0901111117", "email": "g@example.com", "balance": 6100000},
            {"id": 8, "fullName": "Nguyen Thi H", "phoneNumber": "0901111118", "email": "h@example.com", "balance": 5500000},
            {"id": 9, "fullName": "Tran Van I", "phoneNumber": "0901111119", "email": "i@example.com", "balance": 4700000},
            {"id": 10, "fullName": "Pham Thi K", "phoneNumber": "0901111120", "email": "k@example.com", "balance": 5200000},
            {"id": 11, "fullName": "Le Van L", "phoneNumber": "0901111121", "email": "l@example.com", "balance": 3100000},
        ],
    )

    op.bulk_insert(
        TUITION_TABLE,
        [
            {"id": 4, "idTransaction": "TXN004", "studentId": "ST004", "studentName": "Pham Thi D", "tuition": 1600000, "is_paid": False, "paid_at": None},
            {"id": 5, "idTransaction": "TXN005", "studentId": "ST005", "studentName": "Hoang Van E", "tuition": 1900000, "is_paid": True, "paid_at": datetime.utcnow()},
            {"id": 6, "idTransaction": "TXN006", "studentId": "ST006", "studentName": "Le Thi F", "tuition": 1750000, "is_paid": False, "paid_at": None},
            {"id": 7, "idTransaction": "TXN007", "studentId": "ST007", "studentName": "Do Van G", "tuition": 2100000, "is_paid": True, "paid_at": datetime.utcnow()},
            {"id": 8, "idTransaction": "TXN008", "studentId": "ST008", "studentName": "Nguyen Thi H", "tuition": 1850000, "is_paid": False, "paid_at": None},
            {"id": 9, "idTransaction": "TXN009", "studentId": "ST009", "studentName": "Tran Van I", "tuition": 1950000, "is_paid": True, "paid_at": datetime.utcnow()},
            {"id": 10, "idTransaction": "TXN010", "studentId": "ST010", "studentName": "Pham Thi K", "tuition": 2050000, "is_paid": False, "paid_at": None},
            {"id": 11, "idTransaction": "TXN011", "studentId": "ST011", "studentName": "Le Van L", "tuition": 1650000, "is_paid": True, "paid_at": datetime.utcnow()},
        ],
    )

    current_time = datetime.utcnow()
    op.bulk_insert(
        HISTORY_TABLE,
        [
            {"id": 3, "idTransaction": "TXN005", "studentId": "ST005", "tuition": 1900000, "dayComplete": current_time, "payer": "Hoang Van E", "email": "e@example.com", "status": "SUCCESS", "customer_id": 5},
            {"id": 4, "idTransaction": "TXN007", "studentId": "ST007", "tuition": 2100000, "dayComplete": current_time, "payer": "Do Van G", "email": "g@example.com", "status": "SUCCESS", "customer_id": 7},
            {"id": 5, "idTransaction": "TXN009", "studentId": "ST009", "tuition": 1950000, "dayComplete": current_time, "payer": "Tran Van I", "email": "i@example.com", "status": "SUCCESS", "customer_id": 9},
            {"id": 6, "idTransaction": "TXN011", "studentId": "ST011", "tuition": 1650000, "dayComplete": current_time, "payer": "Le Van L", "email": "l@example.com", "status": "SUCCESS", "customer_id": 11},
        ],
    )


def downgrade() -> None:
    op.execute(
        sa.text(
            "DELETE FROM history WHERE idTransaction IN ('TXN005','TXN007','TXN009','TXN011')"
        )
    )
    op.execute(
        sa.text(
            "DELETE FROM tuition WHERE idTransaction IN ('TXN004','TXN005','TXN006','TXN007','TXN008','TXN009','TXN010','TXN011')"
        )
    )
    op.execute(
        sa.text(
            "DELETE FROM CustomerInfor WHERE id IN (4,5,6,7,8,9,10,11)"
        )
    )
    op.execute(
        sa.text(
            "DELETE FROM account WHERE id IN (4,5,6,7,8,9,10,11)"
        )
    )
