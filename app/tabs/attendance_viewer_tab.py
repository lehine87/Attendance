import streamlit as st
import pandas as pd
import calendar
from datetime import datetime
from app.models import Classroom, StudentClassroom, Student, Attendance, ClassSchedule
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def show_attendance_viewer_tab():
    st.header("📅 출결 현황 보기")

    # 1. 월 선택
    today = datetime.today()
    year = st.selectbox("년도 선택", range(today.year, today.year - 5, -1), index=0)
    month = st.selectbox("월 선택", range(1, 13), index=today.month - 1)

    # 2. 반 다중 선택
    classrooms = list(Classroom.select())
    classroom_options = [c.name for c in classrooms]
    selected_class_names = st.multiselect("반 선택", classroom_options)

    if not selected_class_names:
        st.info("반을 하나 이상 선택해주세요.")
        return

    # 3. 구글 시트 연결
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("google_credentials.json", scope)
        gc = gspread.authorize(creds)
        spread = gc.open("유일학원_2025_출석부_이상준")
    except Exception as e:
        st.error(f"Google Sheets 인증 오류: {e}")
        return

    # 4. 반별 출결표 생성 및 출력
    class_dataframes = {}  # 반 이름 → DataFrame

    for class_name in selected_class_names:
        selected_class = next(c for c in classrooms if c.name == class_name)
        st.subheader(f"📘 [{class_name}] 반 출결 현황")

        # 수업 요일 파악
        class_weekdays = set(s.weekday for s in selected_class.schedules)
        weekday_map = {"월": 0, "화": 1, "수": 2, "목": 3, "금": 4, "토": 5, "일": 6}
        weekday_indices = {weekday_map[w] for w in class_weekdays}

        # 수업 날짜만 필터링 + 표시용 날짜 변환
        weekday_str = ["월", "화", "수", "목", "금", "토", "일"]
        _, last_day = calendar.monthrange(year, month)

        date_range = [
            datetime(year, month, day)
            for day in range(1, last_day + 1)
            if datetime(year, month, day).weekday() in weekday_indices
        ]

        # 내부용 key는 ISO 날짜, 표시용은 보기 좋게
        date_keys = [d.strftime("%Y-%m-%d") for d in date_range]
        date_display = [f"{d.month}/{d.day} ({weekday_str[d.weekday()]})" for d in date_range]
        date_columns_map = dict(zip(date_keys, date_display))  # 매핑용 dict


        # 학생 목록
        students = (
            Student.select()
            .join(StudentClassroom)
            .where(StudentClassroom.classroom == selected_class)
            .order_by(Student.name)
        )
        student_names = [s.name for s in students]

        # 출결 데이터프레임 초기화
        df = pd.DataFrame(index=student_names, columns=date_keys)

        attendance_qs = (
            Attendance.select()
            .where(
                (Attendance.classroom == selected_class) &
                (Attendance.date.between(date_range[0], date_range[-1]))
            )
        )
        symbol = {"출석": "○", "지각": "△", "결석": "/", "조퇴": "←"}

        for record in attendance_qs:
            sname = record.student.name
            dstr = record.date.strftime("%Y-%m-%d")
            if sname in df.index and dstr in df.columns:
                df.loc[sname, dstr] = symbol.get(record.status, "")

        df.fillna("", inplace=True)

        # 오늘 날짜에 해당하는 열 이름
        today_key = today.strftime("%Y-%m-%d")
        today_display = date_columns_map.get(today_key, "")

        # 시각화용 열 이름 변환
        df_for_display = df.copy()
        df_for_display.columns = [date_columns_map.get(col, col) for col in df.columns]

        # 오늘 날짜 하이라이트
        def highlight_today(val):
            return ["background-color: yellow" if c == today_display else "" for c in df_for_display.columns]

        st.dataframe(df_for_display.style.apply(highlight_today, axis=1))

        # 저장용 dict에 보관
        class_dataframes[class_name] = df

    # 5. 저장 버튼 (반복문 바깥에 하나만)
    if st.button("📤 전체 반 시트 저장"):
        sheet_title = f"{year}-{month:02d}"

        try:
            try:
                ws = spread.worksheet(sheet_title)
                spread.del_worksheet(ws)
            except gspread.exceptions.WorksheetNotFound:
                pass

            ws = spread.add_worksheet(title=sheet_title, rows=1000, cols=40)
            current_row = 1

            for class_name in selected_class_names:
                df = class_dataframes[class_name]

                header = [f"[{class_name}] 반 출결 현황"]
                date_row = ["이름"] + df.columns.tolist()
                data_rows = df.reset_index().values.tolist()

                ws.update(f"A{current_row}", [header])
                current_row += 1
                ws.update(f"A{current_row}", [date_row])
                current_row += 1
                ws.update(f"A{current_row}", data_rows)
                current_row += len(data_rows) + 2

            st.success(f"✅ Google Sheets 저장 완료: 시트 '{sheet_title}'")
        except Exception as e:
            st.error(f"❌ 저장 실패: {e}")
