# app/tabs/student_tab.py
import streamlit as st
import datetime
from app.models import Student, School
from peewee import IntegrityError

def show_student_tab():
    st.header("👤 학생 등록")

    name = st.text_input("이름")
    grade_level = st.selectbox("학제", ["중", "고", "재수"])
    school_options = {s.name: s.id for s in School.select()}
    school_name = st.selectbox("학교", list(school_options.keys()))
    school_id = school_options[school_name]
    school_year = st.number_input("학년", min_value=1, max_value=6)
    contact_student = st.text_input("학생 연락처")
    contact_parent = st.text_input("학부모 연락처")
    joined_at = st.date_input("입반일", datetime.date.today())
    paused_at = st.date_input("휴원일 (선택)", value=None, disabled=False)

    if st.button("학생 등록"):
        try:
            Student.create(
                name=name,
                grade_level=grade_level,
                school=school_id,
                school_year=school_year,
                joined_at=joined_at,
                paused_at=paused_at if paused_at != joined_at else None,
                contact_student=contact_student,
                contact_parent=contact_parent
            )
            st.success(f"{name} 학생 등록 완료")
        except IntegrityError as e:
            st.error(f"등록 실패: {e}")
