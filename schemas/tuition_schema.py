from datetime import datetime
from pydantic import BaseModel


class TuitionInquiry(BaseModel):
    studentId: str


class TuitionInfor(BaseModel):
    idTransaction: str
    studentId: str
    studentName: str
    tuition: float
    is_paid: bool
    paid_at: datetime | None


class TuitionOtpRequest(BaseModel):
    transaction_id: str
    customer_id: int
    
class TuitionOtpVerify(BaseModel):
    transaction_id: str
    otp_input: str


class TuitionPaymentRequest(BaseModel):
    transaction_id: str
    customer_id: int
    otp_code: str


class PaymentHistoryItem(BaseModel):
    transaction_id: str
    student_id: str
    student_name: str
    tuition: float
    paid_at: datetime
    payer: str
    email: str | None
    status: str
