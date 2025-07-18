# app/init_schema.py
import sqlite3
from pathlib import Path

DB_PATH = Path("data/attendance.db")
DB_PATH.parent.mkdir(exist_ok=True)

def create_tables():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. 학교
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS schools (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        address TEXT,
        math_teacher TEXT,
        science_teacher TEXT
    );
    """)

    # 2. 시험지
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS school_exam_files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        school_id INTEGER,
        year INTEGER,
        file_path TEXT,
        FOREIGN KEY (school_id) REFERENCES schools(id)
    );
    """)

    # 3. 학생
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        grade_level TEXT,  -- 중/고/재수
        school_id INTEGER,
        school_year INTEGER,
        joined_at DATE,
        paused_at DATE,
        contact_student TEXT,
        contact_parent TEXT,
        FOREIGN KEY (school_id) REFERENCES schools(id)
    );
    """)

    # 4. 강사
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS teachers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        contact TEXT,
        joined_at DATE,
        left_at DATE,
        address TEXT
    );
    """)

    # 5. 과목
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subjects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    );
    """)

    # 6. 클래스
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS classrooms (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        grade_level TEXT,  -- 중/고/재수
        subject_id INTEGER,
        book TEXT,
        FOREIGN KEY (subject_id) REFERENCES subjects(id)
    );
    """)

    # 7. 클래스 요일별 시간
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS class_schedules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        classroom_id INTEGER,
        weekday TEXT,  -- 월, 화, 수 ...
        time TEXT,     -- 예: 16:30~19:00
        FOREIGN KEY (classroom_id) REFERENCES classrooms(id)
    );
    """)

    # 8. 학생-클래스 (M:N)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS student_classrooms (
        student_id INTEGER,
        classroom_id INTEGER,
        PRIMARY KEY (student_id, classroom_id),
        FOREIGN KEY (student_id) REFERENCES students(id),
        FOREIGN KEY (classroom_id) REFERENCES classrooms(id)
    );
    """)

    # 9. 클래스-강사 (M:N) + 역할
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS classroom_teachers (
        classroom_id INTEGER,
        teacher_id INTEGER,
        role TEXT,  -- '담당' or '조교'
        PRIMARY KEY (classroom_id, teacher_id, role),
        FOREIGN KEY (classroom_id) REFERENCES classrooms(id),
        FOREIGN KEY (teacher_id) REFERENCES teachers(id)
    );
    """)

    # 10. 출결 기록
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendances (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        classroom_id INTEGER,
        date DATE,
        status TEXT,  -- 출석, 지각, 결석, 조퇴
        UNIQUE (student_id, classroom_id, date),
        FOREIGN KEY (student_id) REFERENCES students(id),
        FOREIGN KEY (classroom_id) REFERENCES classrooms(id)
    );
    """)

    conn.commit()
    conn.close()
    print(f"✅ DB 스키마 생성 완료: {DB_PATH}")

if __name__ == "__main__":
    create_tables()
