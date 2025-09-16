from datetime import datetime, timedelta
from decimal import Decimal
import secrets

from repositories.tuition_repo import tuitionRepository
from repositories.account_repo import AccountRepository
from schemas.tuition_schema import TuitionInfor


class TuitionService:
    def __init__(self, tuition_repo: tuitionRepository, account_repo: AccountRepository):
        self.tuition_repo = tuition_repo
        self.account_repo = account_repo

    def getTuitionByStudentId(self, student_id: str):
        tuition_records = self.tuition_repo.get_unpaid_tuitions_by_student(student_id)
        if not tuition_records:
            return {"message": "All tuition were complete or don't have any tuition for this student"}
        return [TuitionInfor(**record).model_dump() for record in tuition_records]

    def request_payment_otp(self, transaction_id: str, customer_id: int):
        tuition = self.tuition_repo.get_tuition_by_transaction(transaction_id)
        if not tuition:
            return {"message": "Cannot find tuition information for this transaction"}

        if tuition["is_paid"]:
            return {"message": "This tuition has already been completed"}

        customer = self.account_repo.get_customer_with_balance(customer_id)
        if not customer:
            return {"message": "Cannot find customer information"}

        otp_code = f"{secrets.randbelow(1_000_000):06d}"
        expires_at = datetime.utcnow() + timedelta(minutes=5)

        self.tuition_repo.create_payment_otp(transaction_id, otp_code, expires_at)

        # TODO: integrate email service to send OTP to customer["email"]
        return {
            "transaction_id": transaction_id,
            "studentId": tuition["studentId"],
            "tuition": float(tuition["tuition"]),
            "otp": otp_code,
            "expires_at": expires_at.isoformat(),
            "message": "OTP generated successfully and should be sent to the payer's email",
        }

    def confirm_payment(self, transaction_id: str, customer_id: int, otp_code: str):
        now = datetime.utcnow()

        with self.tuition_repo.db.begin():
            tuition = self.tuition_repo.lock_tuition_by_transaction(transaction_id)
            if not tuition:
                return {"message": "Cannot find tuition information for this transaction"}

            if tuition["is_paid"]:
                return {"message": "This tuition has already been completed"}

            otp_record = self.tuition_repo.get_latest_otp(transaction_id)
            if not otp_record:
                return {"message": "OTP has not been generated for this transaction"}

            if otp_record["verified_at"] is not None:
                return {"message": "This OTP was already used"}

            if otp_record["expires_at"] < now:
                return {"message": "OTP has expired"}

            if otp_record["otp_code"] != otp_code:
                return {"message": "Invalid OTP"}

            customer = self.account_repo.lock_customer_for_update(customer_id)
            if not customer:
                return {"message": "Cannot find customer information"}

            tuition_amount = Decimal(tuition["tuition"])
            current_balance = Decimal(customer["balance"])

            if current_balance < tuition_amount:
                return {"message": "Balance is not enough to cover this tuition"}

            new_balance = current_balance - tuition_amount

            self.account_repo.update_customer_balance(customer_id, new_balance)
            self.tuition_repo.mark_tuition_paid(transaction_id, now)
            self.tuition_repo.insert_history_entry(
                transaction_id=transaction_id,
                student_id=tuition["studentId"],
                tuition_amount=tuition_amount,
                completed_at=now,
                payer_name=customer["fullName"],
                email=customer["email"],
                customer_id=customer_id,
            )
            self.tuition_repo.mark_otp_verified(otp_record["id"], now)

        return {
            "transaction_id": transaction_id,
            "studentId": tuition["studentId"],
            "paid_at": now.isoformat(),
            "tuition": float(tuition_amount),
            "balance_after": float(new_balance),
            "message": "Tuition payment completed successfully",
        }
