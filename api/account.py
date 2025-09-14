from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from sqlalchemy import text
from core.connDB import connDB  # chỉnh đường dẫn nếu cần

# Khởi tạo router
account_router = APIRouter()
db_conn = connDB()  # khởi tạo kết nối DB
        
@account_router.post("/login")
def login(
    user_name: str = Body(...),   # bắt buộc có key "user_name"
    password: str = Body(...),
    db : Session = Depends(db_conn.get_db) # bắt buộc có key "password"
):
    if (not user_name or not password):
        return None
    
    query_verify = text("SELECT * FROM account where userName = :user_name")
    
    result = db.execute(query_verify, {"user_name": user_name}).mappings().first()
    if not result:
        return {"message": "Invalid username or password"}

    if (result["password"] == password):
        return result["id"]
    return {"message": "Invalid username or password"}
