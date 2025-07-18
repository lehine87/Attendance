# app/tabs/enroll_tab.py

import streamlit as st
from app.models import Classroom, Student, StudentClassroom
from peewee import DoesNotExist

def show_enroll_tab():
    st.header("🧩 반-학생 연결 관리")

    # 1. 반 선택
    classrooms = Classroom.select()
    if not classrooms.exists():
        st.warning("⚠️ 등록된 반이 없습니다. 먼저 반을 등록하세요.")
        return

    class_options = {c.name: c.id for c in classrooms}
    selected_class_label = st.selectbox("📘 반 선택", list(class_options.keys()))
    selected_classroom = Classroom.get_by_id(class_options[selected_class_label])

    st.markdown("---")

    # 2. 해당 반의 등록된 학생 목록 (해제 가능)
    st.subheader(f"📋 '{selected_class_label}' 반에 등록된 학생")

    registered_students = (
        Student.select()
        .join(StudentClassroom)
        .where(StudentClassroom.classroom == selected_classroom)
    )

    if registered_students.exists():
        remove_targets = []
        for student in registered_students:
            if st.checkbox(f"{student.name} (ID: {student.id}) ⛔ 해제", key=f"reg_{student.id}"):
                remove_targets.append(student)

        if remove_targets and st.button("🔴 선택한 학생 연결 해제"):
            for s in remove_targets:
                try:
                    link = StudentClassroom.get(
                        StudentClassroom.student == s,
                        StudentClassroom.classroom == selected_classroom
                    )
                    link.delete_instance()
                except DoesNotExist:
                    pass
            st.success(f"🗑️ {len(remove_targets)}명 연결 해제 완료")
    else:
        st.info("이 반에 아직 등록된 학생이 없습니다.")

    st.markdown("---")

    # 3. 등록되지 않은 학생 목록 (등록 가능)
    st.subheader("👤 등록 가능한 학생")

    registered_ids = [s.id for s in registered_students]
    unregistered_students = (
        Student.select()
        .where(Student.id.not_in(registered_ids))
    )

    if not unregistered_students.exists():
        st.success("✅ 모든 학생이 이미 이 반에 등록되어 있습니다.")
    else:
        add_targets = []
        for student in unregistered_students:
            if st.checkbox(f"{student.name} (ID: {student.id}) ✅ 등록", key=f"unreg_{student.id}"):
                add_targets.append(student)

        if add_targets and st.button("👥 선택한 학생 등록"):
            for s in add_targets:
                StudentClassroom.create(student=s, classroom=selected_classroom)
            st.success(f"✅ {len(add_targets)}명 등록 완료")
