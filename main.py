# app/test_insert.py
from app.models import (
    db, School, Subject, Student, Teacher, Classroom,
    StudentClassroom, ClassroomTeacher, Attendance
)
import datetime

db.connect()

# 1. 과목 생성
math = Subject.create(name="수학")

# 2. 학교 생성
school = School.create(
    name="서울과학고",
    address="서울시 종로구",
    math_teacher="이수학",
    science_teacher="박과학"
)

# 3. 학생 생성
student = Student.create(
    name="홍길동",
    grade_level="고",
    school=school,
    school_year=2,
    joined_at="2024-03-01",
    paused_at=None,
    contact_student="010-1234-5678",
    contact_parent="010-9876-5432"
)

# 4. 강사 생성
teacher = Teacher.create(
    name="김선생",
    contact="010-1111-2222",
    joined_at="2023-09-01",
    address="서울시 강남구"
)

# 5. 클래스 생성
classroom = Classroom.create(
    name="고2 수학심화반",
    grade_level="고",
    subject=math,
    book="블랙라벨 수학II"
)

# 6. 학생-반 연결
StudentClassroom.create(
    student=student,
    classroom=classroom
)

# 7. 클래스-강사 연결
ClassroomTeacher.create(
    classroom=classroom,
    teacher=teacher,
    role="담당"
)

# 8. 출결 기록
Attendance.create(
    student=student,
    classroom=classroom,
    date=datetime.date.today(),
    status="출석"
)

db.close()
print("✅ 테스트 데이터 삽입 완료")
