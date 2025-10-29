from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.connDB import connDB
from repositories.account_repo import AccountRepository
from services.account_service import AccountService
from schemas.account_schema import LoginRequest
from fastapi.security import OAuth2PasswordRequestForm

account_router = APIRouter()
db_conn = connDB()

@account_router.get("/")
def test_acc():
    return "Account success"

@account_router.post("/login")
def login(request: LoginRequest, db: Session = Depends(db_conn.get_db)):
    print("🧩 DEBUG: Body nhận được từ client:", request)
    print("🧩 Kiểu dữ liệu:", type(request))
    service = AccountService(AccountRepository(db))
    return service.login(request.username, request.password)

@account_router.post("/login_form")
def login_form(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(db_conn.get_db)):
    service = AccountService(AccountRepository(db))
    return service.login(form_data.username, form_data.password)

@account_router.post("/logout")
def logout(username: str, db: Session = Depends(db_conn.get_db)):
    service = AccountService(AccountRepository(db))
    return service.logout(username)