from passlib.context import CryptContext
from repositories.account_repo import AccountRepository
from schemas.account_schema import Infor
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt

from fastapi import Depends, HTTPException, status
from services.jwt_service import jwt_service_instance
from pwdlib import PasswordHash
from pwdlib.hashers import bcrypt, argon2

class AccountService:
    def __init__(self, repo: AccountRepository):
        self.repo = repo
        # self.context_pwd = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__ident="2b")
        
        # Support legacy bcrypt hashes and future argon2 hashes
        self.context_pwd = PasswordHash((argon2.Argon2Hasher(), bcrypt.BcryptHasher()))
        self.jwt_services = jwt_service_instance
        

    def login(self, username: str, password: str):
        account_auth = self.repo.get_pass_by_username(username)
        # return account['password']
        if not account_auth:
            return {"message": "Invalid username or password"}

        if not self.context_pwd.verify(password, account_auth['password']):
            return {"message": "Invalid username or password"}

        account = self.repo.get_account_by_username(username)
        customer = self.repo.get_customer_infor(account["id"])
        if not customer:
            return {"message": "Cannot find infor !!"}
        
        token_data = {"sub": username}
        if (not self.jwt_services.is_token_active(username)):
            access_token = self.jwt_services.get_token(token_data)
        else:
            self.remove_token(username)
            return {"message": "Account already logged in elsewhere !! Login again."}
        
        
        return {
            "user_infor": Infor(**customer).model_dump(),
            "access_token": access_token
            } 
        
    def remove_token(self, username: str):
        """Xóa session cũ của user trong Redis"""
        self.jwt_services.remove_token(username)
        
    def logout(self, username: str):
        if self.jwt_services.is_token_active(username):
            self.remove_token(username)
            return {"message": "Logout successful"}
        else:
            return {"message": "User is not logged in"}
        
    def get_profile(self, username: str, customer_id: int):
        account = self.repo.get_account_by_username(username)
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Không tìm thấy tài khoản.",
            )

        if account["id"] != customer_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Bạn không có quyền truy cập thông tin khách hàng này.",
            )

        customer = self.repo.get_customer_infor(customer_id)
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Không tìm thấy thông tin khách hàng.",
            )

        return Infor(**customer).model_dump()
    
    
