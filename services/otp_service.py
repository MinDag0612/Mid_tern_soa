from datetime import datetime, timedelta
import secrets

from repositories.tuition_repo import tuitionRepository
from repositories.account_repo import AccountRepository


class OtpService:
    def __init__(self, tuition_repo: tuitionRepository, account_repo: AccountRepository):
        self.tuition_repo = tuition_repo
        self.account_repo = account_repo

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
