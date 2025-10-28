from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from core.connDB import connDB
from services.otp_service import OtpService
from repositories.tuition_repo import tuitionRepository
from repositories.account_repo import AccountRepository
from schemas.tuition_schema import TuitionOtpRequest
from schemas.tuition_schema import TuitionOtpRequest, TuitionOtpVerify


otp_router = APIRouter()
db_conn = connDB()


def _get_service(db: Session) -> OtpService:
    tuition_repo = tuitionRepository(db)
    account_repo = AccountRepository(db)
    return OtpService(tuition_repo, account_repo)

@otp_router.get("/")
def test():
    return "OTP successful"


@otp_router.post("/request-otp")
def request_otp(payload: TuitionOtpRequest, db: Session = Depends(db_conn.get_db)):
    service = _get_service(db)
    result = service.request_payment_otp(payload.transaction_id, payload.customer_id)
    if isinstance(result, tuple) and len(result) == 2:
        body, status = result
        return JSONResponse(content=body, status_code=status)
    return result

@otp_router.post("/verify-otp")
def verify_otp_api(verify_infor: TuitionOtpVerify, db: Session = Depends(db_conn.get_db)):
    service = _get_service(db)
    result = service.verify_otp(verify_infor.transaction_id, verify_infor.otp_input)
    if isinstance(result, tuple) and len(result) == 2:
        body, status = result
        return JSONResponse(content=body, status_code=status)
    return result
