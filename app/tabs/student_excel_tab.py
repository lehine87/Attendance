import streamlit as st
import pandas as pd
from datetime import datetime
from app.models import Student, School
from peewee import IntegrityError

def show_student_excel_tab():
    st.header("📁 엑셀로 학생 일괄 등록")

    st.markdown("""
    - 아래 양식대로 작성된 `.xlsx` 또는 `.csv` 파일을 업로드해주세요.  
    - 필수 열: 이름, 학제, 학년, 학교명, 학생연락처, 학부모연락처, 입반일  
    - 휴원일은 선택입니다.
    """)

    uploaded_file = st.file_uploader("엑셀 파일 업로드", type=["xlsx", "csv"])

    if uploaded_file:
        try:
            if uploaded_file.name.endswith("xlsx"):
                df = pd.read_excel(uploaded_file)
            else:
                df = pd.read_csv(uploaded_file)
        except Exception as e:
            st.error(f"❌ 파일 읽기 실패: {e}")
            return

        st.dataframe(df)

        if st.button("👤 학생 일괄 등록 시작"):
            success_count = 0
            fail_count = 0
            messages = []

            for idx, row in df.iterrows():
                try:
                    school, _ = School.get_or_create(name=row["학교명"])
                    paused_at = row.get("휴원일", None)
                    Student.create(
                        name=row["이름"],
                        grade_level=row["학제"],
                        school=school,
                        school_year=int(row["학년"]),
                        joined_at=pd.to_datetime(row["입반일"]).date(),
                        paused_at=pd.to_datetime(paused_at).date() if pd.notna(paused_at) else None,
                        contact_student=row["학생연락처"],
                        contact_parent=row["학부모연락처"]
                    )
                    success_count += 1
                except Exception as e:
                    fail_count += 1
                    messages.append(f"{idx+1}행 등록 실패: {e}")

            st.success(f"✅ 등록 완료: {success_count}명")
            if fail_count > 0:
                st.warning(f"⚠️ 등록 실패: {fail_count}명")
                with st.expander("상세 오류 보기"):
                    for m in messages:
                        st.text(m)
