from pydantic import BaseModel

class Infor(BaseModel):
    id: int
    fullName: str
    email: str
    phoneNumber: str | None = None
    balance: float | None = None

class LoginRequest(BaseModel):
    username: str
    password: str
