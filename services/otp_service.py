from datetime import datetime, timedelta
import secrets

import random
import requests
import os

from repositories.tuition_repo import tuitionRepository
from repositories.account_repo import AccountRepository
from services.jwt_service import jwt_services

class OtpService:
    def __init__(self, tuition_repo: tuitionRepository, account_repo: AccountRepository):
        self.tuition_repo = tuition_repo
        self.account_repo = account_repo

    def request_payment_otp(self, transaction_id: str, customer_id: int):
        tuition = self.tuition_repo.get_tuition_by_transaction(transaction_id)
        if not tuition:
            return {"message": "Cannot find tuition information for this transaction"}, 400

        if tuition["is_paid"]:
            return {"message": "This tuition has already been completed"}, 400

        customer = self.account_repo.get_customer_with_balance(customer_id)
        if not customer:
            return {"message": "Cannot find customer information"}, 400
        
        if customer['balance'] < tuition['tuition']:
            return {"message": "Customer balance can not pay tuition now !!"}, 400

        otp_code = f"{secrets.randbelow(1_000_000):06d}"
        expires_at = datetime.now() + timedelta(minutes=5)

        query_status, err = self.tuition_repo.create_payment_otp(transaction_id, otp_code, expires_at)
        
        if (not query_status):
            return {"message": f"Cannot query OTP. {err}"}, 400
        
        recipient = customer['email']
        subject = "Verify OTP - Check this mail"
        content = f'''
        Your OTP is: {otp_code}
        OTP will be destroy in 5 minites. Please verify before this time.
        Thanks !!
        '''

        url_mailler = f"http://{os.getenv('APP_HOST', '127.0.0.1')}:{os.getenv('APP_PORT', '8000')}/mailler/send-mail"

        body = {
            "recipient": recipient,
            "subject": subject,
            "content": content
        }
        
        jwt_token = jwt_services().get_token({"sub": customer['email']})
        
        headers = {
            "Authorization": f"Bearer {jwt_token}",   # ✅ thêm JWT token vào header
            "Content-Type": "application/json"        # (tuỳ chọn, giúp service đọc JSON)
        }
                
        response = requests.post(url_mailler, json=body, headers=headers)
        
        try:
            mailer_msg = response.json()
        except ValueError:
            mailer_msg = response.text  # khi không phải JSON
        
        return {
            "transaction_id": transaction_id,
            "studentId": tuition["studentId"],
            "tuition": float(tuition["tuition"]),
            "otp": otp_code,
            "expires_at": expires_at.isoformat(),
            "message": f"{response.status_code} - {mailer_msg} - DB: {err}",
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
