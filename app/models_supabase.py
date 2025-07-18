# app/models.py

from peewee import *
from pathlib import Path
import datetime
import os

# ✅ Supabase (PostgreSQL) DB 연결 정보
db = PostgresqlDatabase(
    database=os.getenv("SUPABASE_DB_NAME", "postgres"),
    user=os.getenv("SUPABASE_DB_USER", "postgres"),
    password=os.getenv("SUPABASE_DB_PASSWORD", ""),
    host=os.getenv("SUPABASE_DB_HOST", "db.XXXX.supabase.co"),
    port=int(os.getenv("SUPABASE_DB_PORT", 5432)),
)

class BaseModel(Model):
    class Meta:
        database = db

# === 아래는 SQLite용과 동일 ===

class School(BaseModel):
    name = CharField()
    address = CharField(null=True)
    math_teacher = CharField(null=True)
    science_teacher = CharField(null=True)

    class Meta:
        table_name = "schools"

class SchoolExamFile(BaseModel):
    school = ForeignKeyField(School, backref="exam_files")
    year = IntegerField()
    file_path = CharField()

    class Meta:
        table_name = "school_exam_files"

class Subject(BaseModel):
    name = CharField(unique=True)

    class Meta:
        table_name = "subjects"

class Student(BaseModel):
    name = CharField()
    grade_level = CharField()
    school = ForeignKeyField(School, backref="students", null=True)
    school_year = IntegerField()
    joined_at = DateField(default=datetime.date.today)
    paused_at = DateField(null=True)
    contact_student = CharField()
    contact_parent = CharField()

    class Meta:
        table_name = "students"

class Teacher(BaseModel):
    name = CharField()
    contact = CharField()
    joined_at = DateField(default=datetime.date.today)
    left_at = DateField(null=True)
    address = CharField(null=True)

    class Meta:
        table_name = "teachers"

class Classroom(BaseModel):
    name = CharField()
    grade_level = CharField()
    subject = ForeignKeyField(Subject, backref="classrooms", null=True)
    book = CharField(null=True)

    class Meta:
        table_name = "classrooms"

class ClassSchedule(BaseModel):
    classroom = ForeignKeyField(Classroom, backref="schedules")
    weekday = CharField()
    time = CharField()

    class Meta:
        table_name = "class_schedules"

class StudentClassroom(BaseModel):
    student = ForeignKeyField(Student, backref="classrooms")
    classroom = ForeignKeyField(Classroom, backref="students")

    class Meta:
        table_name = "student_classrooms"
        primary_key = CompositeKey('student', 'classroom')

class ClassroomTeacher(BaseModel):
    classroom = ForeignKeyField(Classroom, backref="teachers")
    teacher = ForeignKeyField(Teacher, backref="classrooms")
    role = CharField()

    class Meta:
        table_name = "classroom_teachers"
        primary_key = CompositeKey('classroom', 'teacher', 'role')

class Attendance(BaseModel):
    student = ForeignKeyField(Student, backref="attendances")
    classroom = ForeignKeyField(Classroom, backref="attendances")
    date = DateField()
    status = CharField()
    memo = TextField(null=True)

    class Meta:
        table_name = "attendances"
        indexes = ((("student", "classroom", "date"), True),)
