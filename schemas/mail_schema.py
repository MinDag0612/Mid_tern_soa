from pydantic import BaseModel

class mail(BaseModel):
    recipient: str
    subject: str
    content: str