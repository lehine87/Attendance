# init_db.py

from app.models_supabase import (
    db, School, SchoolExamFile, Subject, Student, Teacher,
    Classroom, ClassSchedule, StudentClassroom,
    ClassroomTeacher, Attendance
)

def create_tables():
    with db:
        db.drop_tables([
            Attendance,
            ClassroomTeacher,
            StudentClassroom,
            ClassSchedule,
            Classroom,
            Teacher,
            Student,
            Subject,
            SchoolExamFile,
            School,
        ], safe=True)


        db.create_tables([
            School,
            SchoolExamFile,
            Subject,
            Student,
            Teacher,
            Classroom,
            ClassSchedule,
            StudentClassroom,
            ClassroomTeacher,
            Attendance
        ])
        print("✅ Supabase에 테이블 생성 완료!")

if __name__ == "__main__":
    create_tables()
