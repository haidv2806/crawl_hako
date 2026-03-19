# config.py
# Chứa các thông tin cấu hình dùng chung cho dự án

# ================== CẤU HÌNH API ==================
JWT_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyLCJqdGkiOiI3ZjNkMzljNS0xM2FjLTQxOTQtYTMyOC00MjAyMWQ5NWU2MGEiLCJpYXQiOjE3NjQwODg2NTEsImV4cCI6MTc2NjY4MDY1MX0.aHE0VfxuAcV9oaa6wi8zV4_KSq6KatKJAyXB7_d4Emk"
BASE_URL = "http://localhost:3000"

HEADERS = {
    "Authorization": f"Bearer {JWT_TOKEN}"
}
