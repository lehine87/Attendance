# app/models.py
from peewee import *
from pathlib import Path
import datetime

# DB 파일 경로
DB_PATH = Path("data/attendance.db")
DB_PATH.parent.mkdir(exist_ok=True)
db = SqliteDatabase(DB_PATH)

class BaseModel(Model):
    class Meta:
        database = db

# 1. 학교
class School(BaseModel):
    name = CharField()
    address = CharField(null=True)
    math_teacher = CharField(null=True)
    science_teacher = CharField(null=True)

    class Meta:
        table_name = "schools" #테이블명 수동 지정

# 2. 시험지
class SchoolExamFile(BaseModel):
    school = ForeignKeyField(School, backref="exam_files")
    year = IntegerField()
    file_path = CharField()

    class Meta:
        table_name = "school_exam_files" #테이블명 수동 지정

# 3. 과목
class Subject(BaseModel):
    name = CharField(unique=True)

    class Meta:
        table_name = "subjects" #테이블명 수동 지정

# 4. 학생
class Student(BaseModel):
    name = CharField()
    grade_level = CharField()  # 중/고/재수
    school = ForeignKeyField(School, backref="students", null=True)
    school_year = IntegerField()
    joined_at = DateField(default=datetime.date.today)
    paused_at = DateField(null=True)
    contact_student = CharField()
    contact_parent = CharField()

    class Meta:
        table_name = "students" #테이블명 수동 지정

# 5. 강사
class Teacher(BaseModel):
    name = CharField()
    contact = CharField()
    joined_at = DateField(default=datetime.date.today)
    left_at = DateField(null=True)
    address = CharField(null=True)

    class Meta:
        table_name = "teachers" #테이블명 수동 지정

# 6. 클래스
class Classroom(BaseModel):
    name = CharField()
    grade_level = CharField()
    subject = ForeignKeyField(Subject, backref="classrooms", null=True)
    book = CharField(null=True)

    class Meta:
        table_name = "classrooms" #테이블명 수동 지정

# 7. 클래스 요일별 시간
class ClassSchedule(BaseModel):
    classroom = ForeignKeyField(Classroom, backref="schedules")
    weekday = CharField()  # '월', '화', ...
    time = CharField()     # '16:30~19:00'

    class Meta:
        table_name = "class_schedules" #테이블명 수동 지정

# 8. 학생-클래스 연결
class StudentClassroom(BaseModel):
    student = ForeignKeyField(Student, backref="classrooms")
    classroom = ForeignKeyField(Classroom, backref="students")

    class Meta:
        table_name = "student_classrooms"   #테이블명 수동 지정
        primary_key = CompositeKey('student', 'classroom')


# 9. 클래스-강사 연결
class ClassroomTeacher(BaseModel):
    classroom = ForeignKeyField(Classroom, backref="teachers")
    teacher = ForeignKeyField(Teacher, backref="classrooms")
    role = CharField()  # '담당' or '조교'

    class Meta:
        table_name = "classroom_teachers"   #테이블명 수동 지정
        primary_key = CompositeKey('classroom', 'teacher', 'role')

# 10. 출결 기록
class Attendance(BaseModel):
    student = ForeignKeyField(Student, backref="attendances")
    classroom = ForeignKeyField(Classroom, backref="attendances")
    date = DateField()
    status = CharField()  # 출석, 지각, 결석, 조퇴
    memo = TextField(null=True)  # 결석사항, 지각사항, 조퇴사항, 보강계획 적는 용도

    class Meta:
        table_name = "attendances"  #테이블명 수동 지정
        indexes = ((("student", "classroom", "date"), True),)
