from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.connDB import connDB
from services.payment_service import PaymentService
from repositories.tuition_repo import tuitionRepository
from repositories.account_repo import AccountRepository
from schemas.tuition_schema import TuitionPaymentRequest


payment_router = APIRouter()
db_conn = connDB()


def _get_service(db: Session) -> PaymentService:
    tuition_repo = tuitionRepository(db)
    account_repo = AccountRepository(db)
    return PaymentService(tuition_repo, account_repo)


@payment_router.post("/pay")
def confirm_payment(payload: TuitionPaymentRequest, db: Session = Depends(db_conn.get_db)):
    service = _get_service(db)
    return service.confirm_payment(
        payload.transaction_id,
        payload.customer_id,
        payload.otp_code,
    )
