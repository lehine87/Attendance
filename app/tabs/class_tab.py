# app/tabs/class_tab.py

import streamlit as st
from peewee import IntegrityError
from app.models import Classroom, ClassSchedule, Subject, Teacher, ClassroomTeacher

def show_class_tab():
    st.header("🏫 반 등록")

    # 1. 반 기본 정보 입력
    class_name = st.text_input("반 이름")
    grade_level = st.selectbox("학제", ["중", "고", "재수"])
    
    # 과목 선택
    subject_options = {s.name: s.id for s in Subject.select()}
    if not subject_options:
        st.warning("⚠️ 먼저 과목을 등록해야 반을 등록할 수 있습니다.")
        return
    subject_name = st.selectbox("과목", list(subject_options.keys()))
    subject_id = subject_options[subject_name]

    book = st.text_input("사용 교재")

    # 2. 강의 요일 및 시간 입력
    st.subheader("📆 강의 요일 및 시간 설정")
    weekday_inputs = {}
    for day in ['월', '화', '수', '목', '금', '토', '일']:
        col1, col2 = st.columns([1, 3])
        with col1:
            enabled = st.checkbox(day, key=f"{day}_check")
        with col2:
            time_range = st.text_input(f"{day} 수업 시간 (예: 16:30~18:30)", key=f"{day}_time")
        if enabled and time_range:
            weekday_inputs[day] = time_range

    # 3. 강사 선택
    teacher_options = {t.name: t.id for t in Teacher.select()}
    if not teacher_options:
        st.warning("⚠️ 먼저 강사를 등록해야 반을 등록할 수 있습니다.")
        return

    main_teacher_name = st.selectbox("담당 강사", list(teacher_options.keys()))
    assistant_teacher_name = st.selectbox("조교 (선택)", ["없음"] + list(teacher_options.keys()))

    # 4. 등록 버튼
    if st.button("반 등록"):
        try:
            classroom = Classroom.create(
                name=class_name,
                grade_level=grade_level,
                subject=subject_id,
                book=book
            )

            # 강의 요일 등록
            for day, time in weekday_inputs.items():
                ClassSchedule.create(
                    classroom=classroom,
                    weekday=day,
                    time=time
                )

            # 담당 강사 등록
            ClassroomTeacher.create(
                classroom=classroom,
                teacher=teacher_options[main_teacher_name],
                role="담당"
            )

            # 조교 등록 (선택)
            if assistant_teacher_name != "없음":
                ClassroomTeacher.create(
                    classroom=classroom,
                    teacher=teacher_options[assistant_teacher_name],
                    role="조교"
                )

            st.success(f"✅ '{class_name}' 반 등록 완료")

        except IntegrityError as e:
            st.error(f"❌ 등록 실패: {e}")
