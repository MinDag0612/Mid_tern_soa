from repositories.tuition_repo import tuitionRepository
from schemas.tuition_schema import TuitionInfor


class TuitionService:
    def __init__(self, tuition_repo: tuitionRepository):
        self.tuition_repo = tuition_repo

    def getTuitionByStudentId(self, student_id: str):
        tuition_records = self.tuition_repo.get_tuitions_by_student(student_id)
        if not tuition_records:
            return {"message": "Không tìm thấy học phí cho sinh viên này."}
        return [TuitionInfor(**record).model_dump() for record in tuition_records]
