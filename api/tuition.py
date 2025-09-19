from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.connDB import connDB
from services.tuition_service import TuitionService
from repositories.tuition_repo import tuitionRepository
from schemas.tuition_schema import TuitionInquiry


tuition_router = APIRouter()
db_conn = connDB()


def _get_tuition_service(db: Session) -> TuitionService:
    return TuitionService(tuitionRepository(db))

    
@tuition_router.get("/")
def test_acc():
    return "Tuition success"


@tuition_router.post("/getTuition")
def get_tuition(payload: TuitionInquiry, db: Session = Depends(db_conn.get_db)):
    service = _get_tuition_service(db)
    return service.getTuitionByStudentId(payload.studentId)
