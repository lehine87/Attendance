# app/tabs/student_edit_tab.py

import streamlit as st
from app.models import Student, School
from peewee import IntegrityError

def show_student_edit_tab():
    st.header("✏️ 학생 정보 수정")

    students = Student.select()
    if not students.exists():
        st.warning("등록된 학생이 없습니다.")
        return

    student_options = {f"{s.name} (ID: {s.id})": s.id for s in students}
    selected_label = st.selectbox("수정할 학생 선택", list(student_options.keys()))
    student = Student.get_by_id(student_options[selected_label])

    # 현재 값 표시
    name = st.text_input("이름", value=student.name)
    grade_level = st.selectbox("학제", ["중", "고", "재수"], index=["중", "고", "재수"].index(student.grade_level))
    school_options = {s.name: s.id for s in School.select()}
    school_name = [k for k, v in school_options.items() if v == student.school.id][0]
    selected_school = st.selectbox("학교", list(school_options.keys()), index=list(school_options.keys()).index(school_name))
    school_id = school_options[selected_school]
    school_year = st.number_input("학년", min_value=1, max_value=6, value=student.school_year)
    contact_student = st.text_input("학생 연락처", value=student.contact_student)
    contact_parent = st.text_input("학부모 연락처", value=student.contact_parent)

    if st.button("💾 수정 저장"):
        try:
            student.name = name
            student.grade_level = grade_level
            student.school = school_id
            student.school_year = school_year
            student.contact_student = contact_student
            student.contact_parent = contact_parent
            student.save()
            st.success("✅ 수정 완료")
        except IntegrityError as e:
            st.error(f"❌ 수정 실패: {e}")
