from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
import redis
import json
import os.path

class jwt_services:
    def __init__(self):
        self.SECRET_KEY = "your_secret_key"
        self.ALGORITHM = "HS256"
        # self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="accounts/login")
        # self.active_tokens = dict() 
        self.redis = redis.Redis(
            host=os.getenv("REDIS_HOST", "redis"),  # "redis" vì nó là tên service trong docker-compose
            port=int(os.getenv("REDIS_PORT", 6379)),
            decode_responses=True
        )

    def get_token(self, token_data: dict):
        username = token_data["sub"]
        # Thêm thời gian hết hạn (1h)
        expire = datetime.now() + timedelta(hours=1)
        token_data.update({"exp": expire})
        
        access_token = jwt.encode(token_data, self.SECRET_KEY, algorithm=self.ALGORITHM)

        session_data = {
            "token": access_token,
            "created_at": datetime.now().isoformat()
        }
        self.redis.setex(f"user:{username}", timedelta(hours=1), json.dumps(session_data))
        return access_token

    def get_current_user(self, token: str = Depends(OAuth2PasswordBearer(tokenUrl="accounts/login_form"))):
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            username = payload.get("sub")
            if not username:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
            return username

        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
        
    def is_token_active(self, username: str):
        return self.redis.exists(f"user:{username}") == 1

    def remove_token(self, username: str):
        self.redis.delete(f"user:{username}")
    
jwt_service_instance = jwt_services()