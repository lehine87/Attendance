# run_streamlit.ps1

# 1. 가상환경 활성화
. .\.venv_office\Scripts\Activate.ps1

# 2. PYTHONPATH 환경 변수 설정
$env:PYTHONPATH = "."

# 3. Streamlit 앱 실행
streamlit run app/streamlit_app.py
