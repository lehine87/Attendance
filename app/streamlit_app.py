# app/streamlit_app.py

import streamlit as st

# 출결
from app.tabs.attendance_tab import show_attendance_tab
from app.tabs.attendance_viewer_tab import show_attendance_viewer_tab

# 등록 탭
from app.tabs.student_tab import show_student_tab
from app.tabs.student_excel_tab import show_student_excel_tab
from app.tabs.class_tab import show_class_tab
from app.tabs.enroll_tab import show_enroll_tab
from app.tabs.teacher_tab import show_teacher_tab
from app.tabs.subject_tab import show_subject_tab

# 수정 탭
from app.tabs.student_edit_tab import show_student_edit_tab
from app.tabs.class_edit_tab import show_class_edit_tab
from app.tabs.teacher_edit_tab import show_teacher_edit_tab
from app.tabs.subject_edit_tab import show_subject_edit_tab

st.set_page_config(page_title="학생 출결 관리 시스템", layout="wide")

# 메인탭 선택
main_tab = st.sidebar.selectbox("📂 메인 메뉴", ["출결", "등록", "수정"])

if main_tab == "출결":
    sub_tab = st.sidebar.selectbox("출결 기능", ["출결 등록", "출결 현황 조회"])

    if sub_tab == "출결 등록":
        show_attendance_tab()
    elif sub_tab == "출결 현황 조회":
        show_attendance_viewer_tab()

elif main_tab == "등록":
    register_tab = st.sidebar.selectbox("📋 등록 항목", [
        "👤 학생 등록", "📥 학생 일괄 등록", "🏫 반 등록",
        "🧩 반-학생 등록", "🧑‍🏫 강사 등록", "📚 과목 등록"
    ])

    if register_tab == "👤 학생 등록":
        show_student_tab()
    elif register_tab == "📥 학생 일괄 등록":
        show_student_excel_tab()
    elif register_tab == "🏫 반 등록":
        show_class_tab()
    elif register_tab == "🧩 반-학생 등록":
        show_enroll_tab()
    elif register_tab == "🧑‍🏫 강사 등록":
        show_teacher_tab()
    elif register_tab == "📚 과목 등록":
        show_subject_tab()

elif main_tab == "수정":
    edit_tab = st.sidebar.selectbox("✏️ 수정 항목", [
        "학생 수정", "반 수정", "강사 수정", "과목 수정"
    ])

    if edit_tab == "학생 수정":
        show_student_edit_tab()
    elif edit_tab == "반 수정":
        show_class_edit_tab()
    elif edit_tab == "강사 수정":
        show_teacher_edit_tab()
    elif edit_tab == "과목 수정":
        show_subject_edit_tab()
