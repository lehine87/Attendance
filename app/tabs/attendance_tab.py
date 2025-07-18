# app/tabs/attendance_tab.py

import streamlit as st
import datetime
from app.models import (
    Student, Classroom, ClassSchedule, StudentClassroom, Attendance
)

def show_attendance_tab():
    st.header("📅 출결 등록")

    selected_date = st.date_input("출결 날짜", datetime.date.today())
    selected_weekday = selected_date.strftime('%a')
    weekday_kor = {
        'Mon': '월', 'Tue': '화', 'Wed': '수',
        'Thu': '목', 'Fri': '금', 'Sat': '토', 'Sun': '일'
    }[selected_weekday]

    classroom_query = (
        Classroom.select()
        .join(ClassSchedule)
        .where(ClassSchedule.weekday == weekday_kor)
        .distinct()
    )

    if not classroom_query.exists():
        st.info(f"'{weekday_kor}' 요일에 수업이 있는 반이 없습니다.")
        return

    class_options = {c.name: c.id for c in classroom_query}
    selected_class_label = st.selectbox("📘 반 선택", list(class_options.keys()))
    selected_classroom_id = class_options[selected_class_label]
    selected_classroom = Classroom.get_by_id(selected_classroom_id)

    st.subheader(f"👥 {selected_class_label} 학생 출결 등록")

    student_query = (
        Student.select()
        .join(StudentClassroom)
        .where(StudentClassroom.classroom == selected_classroom)
    )

    status_labels = {
        "출석": "✅ 출석",
        "지각": "⏰ 지각",
        "결석": "❌ 결석",
        "조퇴": "🏃 조퇴"
    }

    # 상단에서 입력 상태 저장용 dictionary
    memo_states = {}

    for student in student_query:
        col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
        with col1:
            st.markdown(f"**{student.name}**")

        # 기존 출결 기록 조회
        existing_attendance = Attendance.get_or_none(
            Attendance.student == student,
            Attendance.classroom == selected_classroom,
            Attendance.date == selected_date
        )
        current_status = existing_attendance.status if existing_attendance else None
        current_memo = existing_attendance.memo if existing_attendance else ""

        def mark(status, memo_text=None):
            if current_status == status and (status != "결석" or current_memo == memo_text):
                st.info(f"{student.name} - 이미 '{status}'으로 등록됨")
                return
            if existing_attendance:
                existing_attendance.delete_instance()
            Attendance.create(
                student=student,
                classroom=selected_classroom,
                date=selected_date,
                status=status,
                memo=memo_text if status == "결석" else None
            )
            st.success(f"{student.name} - '{status}'로 저장됨")

        # 버튼 및 ✔️ 상태 표시
        with col2:
            if st.button("✅ 출석", key=f"a_{student.id}"):
                mark("출석")
            if current_status == "출석":
                st.markdown("✔️", unsafe_allow_html=True)

        with col3:
            if st.button("⏰ 지각", key=f"b_{student.id}"):
                mark("지각")
            if current_status == "지각":
                st.markdown("✔️", unsafe_allow_html=True)

        with col4:
            if st.button("❌ 결석", key=f"c_{student.id}"):
                st.session_state[f"memo_active_{student.id}"] = True
            if current_status == "결석":
                st.markdown("✔️", unsafe_allow_html=True)

        with col5:
            if st.button("🏃 조퇴", key=f"d_{student.id}"):
                mark("조퇴")
            if current_status == "조퇴":
                st.markdown("✔️", unsafe_allow_html=True)

        # 메모 입력창 표시 (결석 상태일 경우 or 버튼 클릭했을 경우)
        if current_status == "결석" or st.session_state.get(f"memo_active_{student.id}", False):
            memo_text = st.text_area("결석 사유 및 보강 일정", value=current_memo, key=f"memo_{student.id}")
            if st.button("💾 메모 저장", key=f"save_memo_{student.id}"):
                mark("결석", memo_text)
                st.session_state[f"memo_active_{student.id}"] = False