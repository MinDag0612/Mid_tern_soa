"""Generate fake data for the tuition payment system."""

from __future__ import annotations

import os
from datetime import datetime, timedelta
from random import choice, randint, random

from faker import Faker
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

FAKE = Faker("vi_VN")


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://sa:12345@localhost:3306/TuitionDB",
)


ENGINE = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=ENGINE, future=True)


PASSWORD_HASH = "$2b$12$CQaG1mDCWWwMJ2bAS1gBBub8wA8G1ARqlMRy2oGcuWQzypI6JapBG"


def generate_students(count: int = 20):
    with SessionLocal() as session:
        for i in range(count):
            account_id = session.execute(
                text("SELECT COALESCE(MAX(id), 0) + 1 FROM account")
            ).scalar_one()
            username = f"student{account_id:02d}"
            session.execute(
                text(
                    "INSERT INTO account (id, userName, password) VALUES (:id, :username, :password)"
                ),
                {"id": account_id, "username": username, "password": PASSWORD_HASH},
            )

            name = FAKE.name()
            phone = f"09{randint(10000000, 99999999)}"
            balance = randint(2_000_000, 7_000_000)

            email_unique = False
            while not email_unique:
                email_candidate = FAKE.email()
                existing_email = session.execute(
                    text("SELECT 1 FROM CustomerInfor WHERE email = :email"),
                    {"email": email_candidate},
                ).scalar()
                if not existing_email:
                    email_unique = True
                    email = email_candidate

            session.execute(
                text(
                    """
                    INSERT INTO CustomerInfor (id, fullName, phoneNumber, email, balance)
                    VALUES (:id, :fullName, :phoneNumber, :email, :balance)
                    """
                ),
                {
                    "id": account_id,
                    "fullName": name,
                    "phoneNumber": phone,
                    "email": email,
                    "balance": balance,
                },
            )

            tuition_count = randint(1, 3)
            for _ in range(tuition_count):
                student_code = f"ST{randint(1000, 9999)}"
                amount = choice([1_600_000, 1_800_000, 2_000_000, 2_200_000])
                was_paid = random() < 0.5
                paid_at = datetime.utcnow() - timedelta(days=randint(1, 90)) if was_paid else None
                transaction_id = FAKE.unique.bothify(text="TXN###??").upper()

                session.execute(
                    text(
                        """
                        INSERT INTO tuition (idTransaction, studentId, studentName, tuition, is_paid, paid_at)
                        VALUES (:transaction_id, :student_id, :student_name, :tuition, :is_paid, :paid_at)
                        """
                    ),
                    {
                        "transaction_id": transaction_id,
                        "student_id": student_code,
                        "student_name": name,
                        "tuition": amount,
                        "is_paid": was_paid,
                        "paid_at": paid_at,
                    },
                )

                if was_paid:
                    session.execute(
                        text(
                            """
                            INSERT INTO history (idTransaction, studentId, tuition, dayComplete, payer, email, status, customer_id)
                            VALUES (:transaction_id, :student_id, :tuition, :day_complete, :payer, :email, :status, :customer_id)
                            """
                        ),
                        {
                            "transaction_id": transaction_id,
                            "student_id": student_code,
                            "tuition": amount,
                            "day_complete": paid_at or datetime.utcnow(),
                            "payer": name,
                            "email": email,
                            "status": "SUCCESS",
                            "customer_id": account_id,
                        },
                    )

        session.commit()


def main():
    count = int(os.getenv("FAKE_STUDENT_COUNT", "20"))
    generate_students(count)
    print(f"Inserted {count} fake students (with accounts, tuition, history).")


if __name__ == "__main__":
    main()
