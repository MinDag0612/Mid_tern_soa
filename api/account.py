from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.connDB import connDB
from repositories.account_repo import AccountRepository
from services.account_service import AccountService
from schemas.account_schema import LoginRequest

account_router = APIRouter()
db_conn = connDB()

@account_router.get("/")
def test_acc():
    return "Account success"

@account_router.post("/login")
def login(request: LoginRequest, db: Session = Depends(db_conn.get_db)):
    service = AccountService(AccountRepository(db))
    return service.login(request.user_name, request.password)
