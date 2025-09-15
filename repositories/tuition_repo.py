from sqlalchemy.orm import Session
from sqlalchemy import text

class tuitionRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_tuition_infor_by_studentId(self, studentId: str):
        query = text("SELECT * FROM tuition WHERE studentId = :student_Id")
        return self.db.execute(
            query, {"student_Id": studentId}
        ).mappings().first()