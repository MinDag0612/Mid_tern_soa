from datetime import datetime, timedelta
import secrets

from repositories.tuition_repo import tuitionRepository
from repositories.account_repo import AccountRepository
from api.mailler import send_email_v1

class OtpService:
    def __init__(self, tuition_repo: tuitionRepository, account_repo: AccountRepository):
        self.tuition_repo = tuition_repo
        self.account_repo = account_repo

    def request_payment_otp(self, transaction_id: str, customer_id: int):
        now = datetime.utcnow()
        tuition = self.tuition_repo.lock_tuition_by_transaction(transaction_id)
        if not tuition:
            return {"message": "Cannot find tuition information for this transaction"}, 400

        if tuition["is_paid"]:
            return {"message": "This tuition has already been completed"}, 400

        customer = self.account_repo.get_customer_with_balance(customer_id)
        if not customer:
            return {"message": "Cannot find customer information"}, 400
        
        if customer['balance'] < tuition['tuition']:
            return {"message": "Customer balance can not pay tuition now !!"}, 400

        active_otp = self.tuition_repo.get_active_otp(transaction_id, now)
        if (
            active_otp
            and active_otp.get("requested_by") is not None
            and active_otp["requested_by"] != customer_id
            and active_otp.get("expires_at") > now
        ):
            self.tuition_repo.insert_otp_audit(
                transaction_id,
                customer_id,
                customer.get("email"),
                "REJECTED",
                "Another account is already processing this transaction.",
            )
            self.tuition_repo.db.commit()
            return {
                "message": "Giao dịch này đang được tài khoản khác xử lý. Vui lòng thử lại sau vài phút."
            }, 409

        otp_code = f"{secrets.randbelow(1_000_000):06d}"
        expires_at = now + timedelta(minutes=5)

        query_status, err = self.tuition_repo.create_payment_otp(
            transaction_id,
            otp_code,
            expires_at,
            customer_id,
            now,
        )
        
        if (not query_status):
            self.tuition_repo.insert_otp_audit(
                transaction_id,
                customer_id,
                customer.get("email"),
                "FAILED",
                f"Database error: {err}",
            )
            self.tuition_repo.db.commit()
            return {"message": f"Cannot query OTP. {err}"}, 400
        
        recipient = customer['email']
        subject = "Verify OTP - Check this mail"
        content = f'''
        Your OTP is: {otp_code}
        OTP will be destroy in 5 minites. Please verify before this time.
        Thanks !!
        '''

        mail_sent = send_email_v1(recipient, subject, content)

        if not mail_sent:
            self.tuition_repo.insert_otp_audit(
                transaction_id,
                customer_id,
                recipient,
                "FAILED",
                "Mail service could not send OTP.",
            )
            self.tuition_repo.db.commit()
            return {
                "message": "Không thể gửi email OTP. Vui lòng thử lại sau."
            }, 500

        self.tuition_repo.insert_otp_audit(
            transaction_id,
            customer_id,
            recipient,
            "SENT",
            None,
        )
        self.tuition_repo.db.commit()

        return {
            "transaction_id": transaction_id,
            "studentId": tuition["studentId"],
            "tuition": float(tuition["tuition"]),
            "expires_at": expires_at.isoformat(),
            "message": "OTP đã được gửi qua email.",
        }, 200
        
    def verify_otp(self, transaction_id: str, otp_input: str):
        otp_verify = self.tuition_repo.get_otp_to_verify(transaction_id)
        if not otp_verify:
            return {"message": "OTP not found"}, 404
        if (otp_verify["otp_code"] == otp_input):
            return {
                "message": f"{otp_input} is valid !!"
            }, 200
        return {
            "message": f"{otp_input} is invalid !!"
        }, 400
