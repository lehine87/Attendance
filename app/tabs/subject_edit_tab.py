# app/tabs/subject_edit_tab.py

import streamlit as st
from app.models import Subject
from peewee import IntegrityError

def show_subject_edit_tab():
    st.header("📚 과목 정보 수정")

    subjects = Subject.select()
    if not subjects.exists():
        st.warning("등록된 과목이 없습니다.")
        return

    subject_options = {f"{s.name} (ID: {s.id})": s.id for s in subjects}
    selected = st.selectbox("수정할 과목 선택", list(subject_options.keys()))
    subject = Subject.get_by_id(subject_options[selected])

    new_name = st.text_input("과목 이름", value=subject.name)

    if st.button("💾 과목 정보 수정"):
        try:
            subject.name = new_name
            subject.save()
            st.success("✅ 과목 정보가 성공적으로 수정되었습니다.")
        except IntegrityError as e:
            st.error(f"❌ 저장 실패: {e}")
