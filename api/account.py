from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from sqlalchemy import text
from core.connDB import connDB  # chỉnh đường dẫn nếu cần
from passlib.context import CryptContext

# Khởi tạo router
account_router = APIRouter()
db_conn = connDB()  # khởi tạo kết nối DB
context_pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
@account_router.post("/login")
def login(
    user_name: str = Body(...),
    password: str = Body(...),
    db : Session = Depends(db_conn.get_db) # bắt buộc có key "password"
):
    if (not user_name or not password):
        return None
    
    query_verify = text("SELECT * FROM account where userName = :user_name")
    
    result = db.execute(query_verify, {"user_name": user_name}).mappings().first()
    if not result:
        return {"message": "Invalid username or password"}

    if (context_pwd.verify(password, result["password"])):
        return result["id"]
    return {"message": "Invalid username or password"}

@account_router.get("/")
def testAcc():
    return "Account success"
