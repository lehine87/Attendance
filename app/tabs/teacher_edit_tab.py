# app/tabs/teacher_edit_tab.py

import streamlit as st
from app.models import Teacher
from peewee import IntegrityError

def show_teacher_edit_tab():
    st.header("🧑‍🏫 강사 정보 수정")

    teachers = Teacher.select()
    if not teachers.exists():
        st.warning("등록된 강사가 없습니다.")
        return

    teacher_options = {f"{t.name} (ID: {t.id})": t.id for t in teachers}
    selected = st.selectbox("수정할 강사 선택", list(teacher_options.keys()))
    teacher = Teacher.get_by_id(teacher_options[selected])

    # 필드 입력
    new_name = st.text_input("이름", value=teacher.name)
    new_phone = st.text_input("연락처", value=teacher.phone)
    new_address = st.text_input("주소", value=teacher.address or "")
    new_hire = st.date_input("입사일", value=teacher.hire_date)
    new_retire = st.date_input("퇴사일 (선택)", value=teacher.retire_date or None)

    if st.button("💾 강사 정보 수정"):
        try:
            teacher.name = new_name
            teacher.phone = new_phone
            teacher.address = new_address
            teacher.hire_date = new_hire
            teacher.retire_date = new_retire
            teacher.save()
            st.success("✅ 강사 정보가 성공적으로 수정되었습니다.")
        except IntegrityError as e:
            st.error(f"❌ 저장 실패: {e}")
