import sqlite3

conn = sqlite3.connect("data/attendance.db")
cursor = conn.cursor()

# memo 컬럼이 없다면 추가
try:
    cursor.execute("ALTER TABLE attendances ADD COLUMN memo TEXT;")
    print("✅ memo 필드 추가 완료")
except sqlite3.OperationalError as e:
    print("⚠️ 이미 memo 필드가 존재하거나 다른 오류:", e)

conn.commit()
conn.close()
