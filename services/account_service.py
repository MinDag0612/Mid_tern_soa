from passlib.context import CryptContext
from repositories.account_repo import AccountRepository
from schemas.account_schema import Infor
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt

from fastapi import Depends, HTTPException, status
from services.jwt_service import jwt_services
from pwdlib import PasswordHash
from pwdlib.hashers import bcrypt, argon2

class AccountService:
    def __init__(self, repo: AccountRepository):
        self.repo = repo
        # self.context_pwd = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__ident="2b")
        
        # Support legacy bcrypt hashes and future argon2 hashes
        self.context_pwd = PasswordHash((argon2.Argon2Hasher(), bcrypt.BcryptHasher()))
        

    def login(self, user_name: str, password: str):
        account_auth = self.repo.get_pass_by_username(user_name)
        # return account['password']
        if not account_auth:
            return {"message": "Invalid username or password"}

        if not self.context_pwd.verify(password, account_auth['password']):
            return {"message": "Invalid username or password"}

        account = self.repo.get_account_by_username(user_name)
        customer = self.repo.get_customer_infor(account["id"])
        if not customer:
            return {"message": "Cannot find infor !!"}
        
        token_data = {"sub": user_name}
        access_token = jwt_services().get_token(token_data)
        
        return {
            "user_infor": Infor(**customer).model_dump(),
            "access_token": access_token
            } 
        
        
    
    
