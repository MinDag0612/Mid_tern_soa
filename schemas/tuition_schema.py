from pydantic import BaseModel
class studentId(BaseModel):
    studentId: str

class TuitionInfor(BaseModel):
    idTransaction: str
    studentId: str
    studentName: str
    tuition: float