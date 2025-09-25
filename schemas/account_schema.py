from pydantic import BaseModel

class Infor(BaseModel):
    id: int
    fullName: str
    email: str

class LoginRequest(BaseModel):
    user_name: str
    password: str
