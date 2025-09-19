import secrets
from threading import Timer

class OTP:
    def __init__(self):
        self.otp_list = {}
        
    def delete_opt(self, idTransaction):
        self.otp_list.pop(idTransaction, None)
        
    def generate_otp(self, idTransaction: str):
        otp = f"{secrets.randbelow(10**6):06d}"
        self.otp_list[idTransaction] = otp
        Timer(600.0, self.delete_otp, args=[idTransaction]).start()
        return {"otp": otp}
    
    def verify_otp(self, idTransaction: str, entered_otp: str):
        if self.otp_list[idTransaction] == entered_otp:
            return {"message": "valid"}
        return {"message": "invalid"}