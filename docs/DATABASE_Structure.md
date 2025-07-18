# ✅ 전체 시스템 구조 요약
## 🧩 주요 엔터티 (5개)
* Student (학생)
* Classroom (클래스/반)
* Teacher (강사/조교)
* School (학교)
* Attendance (출결 기록)

## 📌 연동 관계 (요약)
* 한 학생은 여러 클래스에 소속될 수 있음 (M:N)
* 한 클래스는 여러 강사와 조교를 가질 수 있음 (M:N)
* 한 강사는 여러 클래스 담당 가능 (M:N)
* 한 학교는 여러 학생과 연결됨 (1:N)
* 출결은 학생 × 클래스 × 날짜로 관리됨

# 📘 Step 1. DB 설계 (ERD 요약)
## 1️⃣ 학생 테이블 students
|필드명|	타입|	설명|
|---|---|---|
|id	|INTEGER|	PK|
|name|	TEXT|	학생 이름|
|grade_level|	TEXT|	학제 (중, 고, 재수)|
|school_id|	INTEGER|	FK → schools.id|
|school_year|	INTEGER|	현재 학년|
|joined_at|	DATE|	입반일|
|paused_at|	DATE|	휴원일 (nullable)|
|contact_student|	TEXT|	학생 연락처|
|contact_parent|	TEXT|	학부모 연락처|

## 2️⃣ 클래스 테이블 classrooms
| 필드명          | 타입      | 설명                 |
| ------------ | ------- | ------------------ |
| id           | INTEGER | PK                 |
| name         | TEXT    | 반 이름               |
| grade\_level | TEXT    | 학제                 |
| subject\_id  | INTEGER | FK → `subjects.id` |
| book         | TEXT    | 사용 교재              |


## 3️⃣ 클래스 요일별 시간 테이블 class_schedules
| 필드명           | 타입      | 설명                           |
| ------------- | ------- | ---------------------------- |
| id            | INTEGER | PK                           |
| classroom\_id | INTEGER | FK → `classrooms.id`         |
| weekday       | TEXT    | 요일 (월\~일)                    |
| time          | TEXT    | 시작시간~~종료시간 (예: 16:30~~19:00) |


## 4️⃣ 학생-클래스 연결 student_classrooms
| 필드명           | 타입      | 설명 |
| ------------- | ------- | -- |
| student\_id   | INTEGER | FK |
| classroom\_id | INTEGER | FK |


## 5️⃣ 강사 테이블 teachers
| 필드명        | 타입      | 설명             |
| ---------- | ------- | -------------- |
| id         | INTEGER | PK             |
| name       | TEXT    | 이름             |
| contact    | TEXT    | 연락처            |
| joined\_at | DATE    | 입사일            |
| left\_at   | DATE    | 퇴사일 (nullable) |
| address    | TEXT    | 주소             |


## 6️⃣ 클래스-강사 연결 classroom_teachers
| 필드명           | 타입      | 설명               |
| ------------- | ------- | ---------------- |
| classroom\_id | INTEGER | FK               |
| teacher\_id   | INTEGER | FK               |
| role          | TEXT    | `'담당'` or `'조교'` |


## 7️⃣ 학교 테이블 schools
| 필드명              | 타입      | 설명                |
| ---------------- | ------- | ----------------- |
| id               | INTEGER | PK                |
| name             | TEXT    | 학교명               |
| address          | TEXT    | 주소                |
| math\_teacher    | TEXT    | 수학 교사명 (nullable) |
| science\_teacher | TEXT    | 과학 교사명 (nullable) |


## 8️⃣ 시험지 테이블 school_exam_files
| 필드명        | 타입      | 설명          |
| ---------- | ------- | ----------- |
| id         | INTEGER | PK          |
| school\_id | INTEGER | FK          |
| year       | INTEGER | 연도          |
| file\_path | TEXT    | 파일 경로 또는 링크 |


## 9️⃣ 출결 테이블 attendances
| 필드명           | 타입      | 설명                             |
| ------------- | ------- | ------------------------------ |
| id            | INTEGER | PK                             |
| student\_id   | INTEGER | FK                             |
| classroom\_id | INTEGER | FK                             |
| date          | DATE    | 날짜                             |
| status        | TEXT    | 출결 상태 (`출석`, `지각`, `결석`, `조퇴`) |

