# app/init_orm.py
from app.models import *

def init_orm_db():
    db.connect()
    db.create_tables([
        School, SchoolExamFile, Subject, Student,
        Teacher, Classroom, ClassSchedule,
        StudentClassroom, ClassroomTeacher, Attendance
    ])
    print("✅ ORM 기반 DB 테이블 생성 완료")
    db.close()

if __name__ == "__main__":
    init_orm_db()
