# app/tabs/class_edit_tab.py

import streamlit as st
import re
from peewee import IntegrityError
from app.models import (
    Classroom, Subject, ClassSchedule,
    Teacher, ClassroomTeacher
)

def show_class_edit_tab():
    st.header("✏️ 반 정보 + 수업 시간표 + 담당자 수정")

    classrooms = Classroom.select()
    if not classrooms.exists():
        st.warning("등록된 반이 없습니다.")
        return

    # 1. 반 선택
    class_options = {f"{c.name} (ID: {c.id})": c.id for c in classrooms}
    selected_label = st.selectbox("수정할 반 선택", list(class_options.keys()))
    classroom = Classroom.get_by_id(class_options[selected_label])

    # 2. 과목 목록
    subject_options = {s.name: s.id for s in Subject.select()}
    current_subject_name = [k for k, v in subject_options.items() if v == classroom.subject.id][0]

    # 3. 기본 반 정보 수정
    new_name = st.text_input("반 이름", value=classroom.name)
    new_grade_level = st.selectbox("학제", ["중", "고", "재수"], index=["중", "고", "재수"].index(classroom.grade_level))
    new_book = st.text_input("사용 교재", value=classroom.book or "")
    new_subject_name = st.selectbox("과목", list(subject_options.keys()), index=list(subject_options.keys()).index(current_subject_name))
    new_subject_id = subject_options[new_subject_name]

    st.markdown("---")
    st.subheader("📆 수업 요일 및 시간 수정")

    # 4. 기존 시간표 불러오기
    existing_schedules = {
        sched.weekday: sched.time
        for sched in ClassSchedule.select().where(ClassSchedule.classroom == classroom)
    }

    # 5. 시간표 수정 입력
    updated_schedule = {}
    for day in ['월', '화', '수', '목', '금', '토', '일']:
        col1, col2 = st.columns([1, 3])
        existing_time = existing_schedules.get(day, "")
        enabled = day in existing_schedules
        with col1:
            enabled = st.checkbox(day, value=enabled, key=f"edit_day_{day}")
        with col2:
            time_str = st.text_input(f"{day} 수업 시간 (예: 16:30~18:30)", value=existing_time, key=f"edit_time_{day}")
        if enabled and time_str:
            if not re.match(r"^\d{1,2}:\d{2}~\d{1,2}:\d{2}$", time_str):
                st.error(f"{day}의 시간 형식이 잘못되었습니다 (예: 16:30~18:30)")
            else:
                updated_schedule[day] = time_str

    st.markdown("---")
    st.subheader("🧑‍🏫 담당 강사 및 조교 수정")

    all_teachers = Teacher.select()
    teacher_options = {f"{t.name} (ID: {t.id})": t.id for t in all_teachers}

    current_teachers = ClassroomTeacher.select().where((ClassroomTeacher.classroom == classroom) & (ClassroomTeacher.role == "강사"))
    current_assistants = ClassroomTeacher.select().where((ClassroomTeacher.classroom == classroom) & (ClassroomTeacher.role == "조교"))

    selected_teacher_ids = st.multiselect(
        "담당 강사",
        list(teacher_options.keys()),
        default=[k for k, v in teacher_options.items() if v in [t.teacher.id for t in current_teachers]]
    )

    selected_assistant_ids = st.multiselect(
        "담당 조교",
        list(teacher_options.keys()),
        default=[k for k, v in teacher_options.items() if v in [a.teacher.id for a in current_assistants]]
    )

    st.markdown("---")

    if st.button("💾 반 정보 전체 저장"):
        try:
            # 반 정보 저장
            classroom.name = new_name
            classroom.grade_level = new_grade_level
            classroom.book = new_book
            classroom.subject = new_subject_id
            classroom.save()

            # 시간표 갱신
            ClassSchedule.delete().where(ClassSchedule.classroom == classroom).execute()
            for day, time_str in updated_schedule.items():
                ClassSchedule.create(classroom=classroom, weekday=day, time=time_str)

            # 기존 강사/조교 삭제 후 재등록
            ClassroomTeacher.delete().where(ClassroomTeacher.classroom == classroom).execute()
            for label in selected_teacher_ids:
                teacher_id = teacher_options[label]
                ClassroomTeacher.create(classroom=classroom, teacher=teacher_id, role="강사")
            for label in selected_assistant_ids:
                teacher_id = teacher_options[label]
                ClassroomTeacher.create(classroom=classroom, teacher=teacher_id, role="조교")

            st.success("✅ 반 정보, 시간표, 담당자 정보까지 모두 수정 완료")

        except IntegrityError as e:
            st.error(f"❌ 저장 실패: {e}")
