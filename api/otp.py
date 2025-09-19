from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.connDB import connDB
from services.otp_service import OtpService
from repositories.tuition_repo import tuitionRepository
from repositories.account_repo import AccountRepository
from schemas.tuition_schema import TuitionOtpRequest


otp_router = APIRouter()
db_conn = connDB()


def _get_service(db: Session) -> OtpService:
    tuition_repo = tuitionRepository(db)
    account_repo = AccountRepository(db)
    return OtpService(tuition_repo, account_repo)


@otp_router.post("/request-otp")
def request_otp(payload: TuitionOtpRequest, db: Session = Depends(db_conn.get_db)):
    service = _get_service(db)
    return service.request_payment_otp(payload.transaction_id, payload.customer_id)
