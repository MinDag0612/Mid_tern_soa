from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import text

class tuitionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_tuition_infor_by_studentId(self, studentId: str):
        records = self.get_tuitions_by_student(studentId)
        for record in records:
            if not record["is_paid"]:
                return record
        return records[0] if records else None

    def get_tuitions_by_student(self, student_id: str):
        query = text(
            """
            SELECT id, idTransaction, studentId, studentName, tuition, is_paid, paid_at
            FROM tuition
            WHERE studentId = :student_id
            ORDER BY created_at ASC
            """
        )
        return self.db.execute(query, {"student_id": student_id}).mappings().all()

    def get_tuition_by_transaction(self, transaction_id: str):
        query = text(
            """
            SELECT id, idTransaction, studentId, studentName, tuition, is_paid, paid_at
            FROM tuition
            WHERE idTransaction = :transaction_id
            """
        )
        return self.db.execute(query, {"transaction_id": transaction_id}).mappings().first()

    def lock_tuition_by_transaction(self, transaction_id: str):
        query = text(
            """
            SELECT id, idTransaction, studentId, studentName, tuition, is_paid, paid_at
            FROM tuition
            WHERE idTransaction = :transaction_id
            FOR UPDATE
            """
        )
        return self.db.execute(query, {"transaction_id": transaction_id}).mappings().first()

    def mark_tuition_paid(self, transaction_id: str, paid_at: datetime):
        query = text(
            """
            UPDATE tuition
            SET is_paid = 1,
                paid_at = :paid_at,
                updated_at = :updated_at
            WHERE idTransaction = :transaction_id
            """
        )
        self.db.execute(
            query,
            {
                "transaction_id": transaction_id,
                "paid_at": paid_at,
                "updated_at": paid_at,
            },
        )

    def insert_history_entry(
        self,
        transaction_id: str,
        student_id: str,
        tuition_amount,
        completed_at: datetime,
        payer_name: str,
        email: str | None,
        customer_id: int | None,
    ):
        query = text(
            """
            INSERT INTO history (idTransaction, studentId, tuition, dayComplete, payer, email, status, customer_id)
            VALUES (:transaction_id, :student_id, :tuition, :day_complete, :payer, :email, :status, :customer_id)
            """
        )
        self.db.execute(
            query,
            {
                "transaction_id": transaction_id,
                "student_id": student_id,
                "tuition": tuition_amount,
                "day_complete": completed_at,
                "payer": payer_name,
                "email": email,
                "status": "SUCCESS",
                "customer_id": customer_id,
            },
        )

    def delete_existing_otps(self, transaction_id: str):
        query = text("DELETE FROM payment_otp WHERE idTransaction = :transaction_id")
        self.db.execute(query, {"transaction_id": transaction_id})

    def create_payment_otp(
        self,
        transaction_id: str,
        otp_code: str,
        expires_at: datetime,
        requested_by: int | None,
        requested_at: datetime,
    ):
        try:
            self.delete_existing_otps(transaction_id)
            query = text(
                """
                INSERT INTO payment_otp (idTransaction, otp_code, expires_at, requested_by, requested_at)
                VALUES (:transaction_id, :otp_code, :expires_at, :requested_by, :requested_at)
                """
            )
            self.db.execute(
                query,
                {
                    "transaction_id": transaction_id,
                    "otp_code": otp_code,
                    "expires_at": expires_at,
                    "requested_by": requested_by,
                    "requested_at": requested_at,
                },
            )
            self.db.commit()
            return True, None
        except Exception as e:
            self.db.rollback()
            return False, str(e)

    def get_active_otp(self, transaction_id: str, current_time: datetime):
        query = text(
            """
            SELECT id, idTransaction, otp_code, expires_at, verified_at, requested_by, requested_at
            FROM payment_otp
            WHERE idTransaction = :transaction_id
              AND verified_at IS NULL
              AND expires_at > :current_time
            ORDER BY created_at DESC
            LIMIT 1
            """
        )
        return self.db.execute(
            query,
            {"transaction_id": transaction_id, "current_time": current_time},
        ).mappings().first()

    def get_otp_to_verify(self, transaction_id: str):
        query = text(
            """
            SELECT otp_code
            FROM payment_otp
            WHERE idTransaction = :transaction_id
            LIMIT 1
            """
        )
        
        return self.db.execute(
            query,
            {
                "transaction_id": transaction_id,
            },
        ).mappings().first()

    def get_latest_otp(self, transaction_id: str):
        query = text(
            """
            SELECT id, idTransaction, otp_code, expires_at, verified_at, created_at, requested_by
            FROM payment_otp
            WHERE idTransaction = :transaction_id
            ORDER BY created_at DESC
            LIMIT 1
            """
        )
        return self.db.execute(query, {"transaction_id": transaction_id}).mappings().first()

    def mark_otp_verified(self, otp_id: int, verified_at: datetime):
        query = text(
            "UPDATE payment_otp SET verified_at = :verified_at WHERE id = :otp_id"
        )
        self.db.execute(query, {"verified_at": verified_at, "otp_id": otp_id})

    def insert_otp_audit(
        self,
        transaction_id: str,
        customer_id: int | None,
        email: str | None,
        status: str,
        detail: str | None,
    ):
        query = text(
            """
            INSERT INTO otp_audit (idTransaction, customer_id, email, status, detail)
            VALUES (:transaction_id, :customer_id, :email, :status, :detail)
            """
        )
        self.db.execute(
            query,
            {
                "transaction_id": transaction_id,
                "customer_id": customer_id,
                "email": email,
                "status": status,
                "detail": detail,
            },
        )

    def get_payment_history_for_customer(
        self,
        customer_id: int,
        limit: int | None = None,
    ):
        limit_clause = ""
        if limit is not None and limit > 0:
            limit_clause = "LIMIT :limit"

        query = text(
            f"""
            SELECT
                h.idTransaction AS transaction_id,
                h.studentId AS student_id,
                t.studentName AS student_name,
                h.tuition AS tuition,
                h.dayComplete AS paid_at,
                h.payer AS payer,
                h.email AS email,
                h.status AS status
            FROM history h
            JOIN tuition t ON t.idTransaction = h.idTransaction
            WHERE h.customer_id = :customer_id
            ORDER BY h.dayComplete DESC
            {limit_clause}
            """
        )
        params = {"customer_id": customer_id}
        if limit_clause:
            params["limit"] = limit
        return self.db.execute(query, params).mappings().all()
