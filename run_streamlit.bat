@echo off
REM 1. 가상환경 활성화
call .\.venv_office\Scripts\activate.bat

REM 2. PYTHONPATH 환경변수 설정
set PYTHONPATH=.

REM 3. Streamlit 앱 실행
streamlit run app\streamlit_app.py

pause
