# 학생 출결 관리 시스템 📅

Streamlit 기반의 학원/학교용 **학생 출결 관리 프로그램**입니다.  
학생, 강사, 반, 과목, 학교 정보를 통합 관리하고, 출결 현황을 직관적으로 조회 및 Google Sheets에 저장할 수 있습니다.

---

## 🏗️ 주요 기능

| 기능 구분 | 세부 기능 |
|----------|-----------|
| 📋 등록 | 학생 등록 / 일괄등록 (엑셀), 반 등록, 강사 등록, 과목 등록 |
| 🔗 연결 | 반-학생 연결 관리 |
| 📝 수정 | 학생, 반, 강사, 과목 정보 수정 |
| ✅ 출결 등록 | 날짜별, 반별 출결 상태 등록 |
| 📊 출결 조회 | 월별 반 출결 현황 확인 및 Google Sheets 저장 |

---

## 🗂️ 폴더 구조

```
.
├── app/
│   ├── streamlit_app.py         # 메인 실행 파일
│   ├── models.py                # Peewee ORM 모델 정의
│   ├── tabs/                    # Streamlit 탭별 UI
│   └── ...                      # 기타 ORM 초기화, Supabase용 모델 등
│
├── data/
│   └── attendance.db            # SQLite 로컬 DB
│
├── docs/
│   ├── DATABASE_Structure.md    # DB 설계 문서
│   └── 출결처리 로직 정의.md     # 출결 처리 로직 문서
│
├── .gitignore
├── main.py                      # 별도 실행 스크립트 (선택사항)
├── run_streamlit.bat           # 윈도우용 실행 스크립트
├── secrets.toml                # Streamlit secrets 설정 파일
└── README.md
```

---

## 🚀 실행 방법

### 1. 가상환경 및 패키지 설치
```bash
python -m venv .venv
source .venv/Scripts/activate      # 윈도우 기준
pip install -r requirements.txt
```

> `requirements.txt`가 없을 경우:
```bash
pip install streamlit peewee pandas gspread oauth2client
```

### 2. Streamlit 실행
```bash
streamlit run app/streamlit_app.py
```

또는 `.bat` 스크립트 사용 (Windows 전용):

```bash
./run_streamlit.bat
```

---

## 📂 DB 및 인증파일

- **SQLite DB**: `data/attendance.db`
- **Google Sheets 인증**: `google_credentials.json` 필요 (secrets.toml 또는 인증 파일 직접 포함)

---

## 📌 향후 확장 예정

- Supabase 기반 온라인 DB 연동 (`models_supabase.py`)
- 학생별 리포트 자동 생성
- 사용자별 권한 설정 (관리자 / 강사)

---

## 📄 라이선스

본 프로젝트는 개인 학원/교습소/학교의 출결 관리를 위한 비상업적 용도로 사용 가능합니다.

---

## 🙋‍♂️ 개발자

이 프로젝트는 [ChatGPT]와 함께 개발되었습니다.  
문의: `sjlee87@kakao.com`