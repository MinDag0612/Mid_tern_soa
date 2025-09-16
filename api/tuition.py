from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.connDB import connDB
from services.tuition_service import TuitionService
from repositories.tuition_repo import tuitionRepository
from repositories.account_repo import AccountRepository
from schemas.tuition_schema import (
    TuitionInquiry,
    TuitionOtpRequest,
    TuitionPaymentRequest,
)

tuition_rounter = APIRouter()
db_conn = connDB()


def _get_service(db: Session) -> TuitionService:
    return TuitionService(tuitionRepository(db), AccountRepository(db))


@tuition_rounter.get("/")
def test_acc():
    return "Tuition success"

@tuition_rounter.post("/getTuition")
def get_tuition(payload: TuitionInquiry, db: Session = Depends(db_conn.get_db)):
    service_tuition = _get_service(db)
    return service_tuition.getTuitionByStudentId(payload.studentId)


@tuition_rounter.post("/request-otp")
def request_otp(payload: TuitionOtpRequest, db: Session = Depends(db_conn.get_db)):
    service_tuition = _get_service(db)
    return service_tuition.request_payment_otp(payload.transaction_id, payload.customer_id)


@tuition_rounter.post("/pay")
def confirm_payment(payload: TuitionPaymentRequest, db: Session = Depends(db_conn.get_db)):
    service_tuition = _get_service(db)
    return service_tuition.confirm_payment(
        payload.transaction_id,
        payload.customer_id,
        payload.otp_code,
    )
