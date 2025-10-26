from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from schemas.OAuth2_schema import oauth2_scheme

class jwt_services:
    def __init__(self):
        self.SECRET_KEY = "your_secret_key" # Cái này là tự cho nên cứ giữ lại
        self.ALGORITHM = "HS256"
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="accounts/login")
    
    def get_token(self, token_data: dict):
        access_token = jwt.encode(token_data, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return access_token
    
    def get_current_user(self, token: str = Depends(oauth2_scheme)):
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            username = payload.get("sub")
            if username is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
            return username
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    # def get_current_user(self, token: str = Depends(OAuth2PasswordBearer(tokenUrl="accounts/login"))):
    #     try:
    #         payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
    #         username = payload.get("sub")
    #         if username is None:
    #             raise HTTPException(
    #                 status_code=status.HTTP_401_UNAUTHORIZED,
    #                 detail="Invalid authentication credentials",
    #             )
    #         return username
    #     except JWTError:
    #         raise HTTPException(
    #             status_code=status.HTTP_401_UNAUTHORIZED,
    #             detail="Invalid authentication credentials",
    #         )
        
