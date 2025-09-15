from repositories.tuition_repo import tuitionRepository
from schemas.tuition_schema import TuitionInfor

class TuitionService:
    def __init__(self, repo: tuitionRepository):
        self.repo = repo
        
    def getTuitionByStudentId(self, studentId: str):
        tuitionInfor = self.repo.get_tuition_infor_by_studentId(studentId)
        if not tuitionInfor:
            return {"message": "All tuition were complete or don't have any tuition for this student"}
        return TuitionInfor(**tuitionInfor).model_dump()