# app/tabs/teacher_tab.py

import streamlit as st
import datetime
from app.models import Teacher
from peewee import IntegrityError

def show_teacher_tab():
    st.header("🧑‍🏫 강사 등록")

    name = st.text_input("이름")
    contact = st.text_input("연락처")
    joined_at = st.date_input("입사일", datetime.date.today())
    left_at = st.date_input("퇴사일 (선택)", value=None, disabled=False)
    address = st.text_input("주소")

    if st.button("강사 등록"):
        try:
            Teacher.create(
                name=name,
                contact=contact,
                joined_at=joined_at,
                left_at=left_at if left_at != joined_at else None,
                address=address
            )
            st.success(f"✅ '{name}' 강사 등록 완료")
        except IntegrityError as e:
            st.error(f"❌ 등록 실패: {e}")

    st.subheader("📋 현재 등록된 강사 목록")
    teachers = Teacher.select()
    if teachers:
        st.dataframe([
            {
                "ID": t.id,
                "이름": t.name,
                "연락처": t.contact,
                "입사일": t.joined_at,
                "퇴사일": t.left_at or "-",
                "주소": t.address
            } for t in teachers
        ])
    else:
        st.info("등록된 강사가 없습니다.")
