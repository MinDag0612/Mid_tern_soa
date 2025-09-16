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


class TuitionPaymentRequest(BaseModel):
    transaction_id: str
    customer_id: int
    otp_code: str
