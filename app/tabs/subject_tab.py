# app/tabs/subject_tab.py

import streamlit as st
from app.models import Subject
from peewee import IntegrityError

def show_subject_tab():
    st.header("📚 과목 등록")

    subject_name = st.text_input("과목명", placeholder="예: 수학, 영어, 화학")

    if st.button("과목 추가"):
        try:
            Subject.create(name=subject_name)
            st.success(f"✅ '{subject_name}' 과목 등록 완료")
        except IntegrityError:
            st.warning(f"⚠️ '{subject_name}' 은 이미 등록된 과목입니다.")

    st.subheader("📖 현재 등록된 과목 목록")
    subjects = Subject.select()
    if subjects:
        st.dataframe([{"ID": s.id, "이름": s.name} for s in subjects])
    else:
        st.info("등록된 과목이 없습니다.")
