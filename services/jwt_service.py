from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta

class jwt_services:
    def __init__(self):
        self.SECRET_KEY = "your_secret_key"
        self.ALGORITHM = "HS256"
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="accounts/login")
        self.active_tokens = dict()  # { username: { token, created_at } }

    def get_token(self, token_data: dict):
        username = token_data["sub"]
        # Thêm thời gian hết hạn (1h)
        expire = datetime.now() + timedelta(hours=1)
        token_data.update({"exp": expire})
        
        access_token = jwt.encode(token_data, self.SECRET_KEY, algorithm=self.ALGORITHM)

        # Ghi đè token cũ của user (chặn login 2 nơi)
        self.active_tokens[username] = {
            "token": access_token,
            "created_at": datetime.now()
        }
        return access_token

    def get_current_user(self, token: str = Depends(OAuth2PasswordBearer(tokenUrl="accounts/login"))):
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            username = payload.get("sub")

            if not username:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

            # Kiểm tra user có tồn tại trong danh sách active token không
            if username not in self.active_tokens:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token not found")

            user_session = self.active_tokens[username]

            # Kiểm tra token có khớp không (chặn login 2 nơi)
            if user_session["token"] != token:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Logged in elsewhere")

            # Kiểm tra thời hạn
            if (datetime.now() - user_session["created_at"]).seconds > 3600:
                del self.active_tokens[username]
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")

            return username

        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
        
    def is_token_active(self, username: str):
        return username in self.active_tokens
    
jwt_service_instance = jwt_services()