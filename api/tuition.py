from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.connDB import connDB
from services.tuition_service import TuitionService
from repositories.tuition_repo import tuitionRepository
from fastapi import Body
from schemas.tuition_schema import studentId

tuition_rounter = APIRouter()
db_conn = connDB()

@tuition_rounter.get("/")
def test_acc():
    return "Tuition success"

@tuition_rounter.post("/getTuition")
def get_tuition(studentId: studentId, db: Session = Depends(db_conn.get_db)):
    service_tuition = TuitionService(tuitionRepository(db))
    return service_tuition.getTuitionByStudentId(studentId.studentId)