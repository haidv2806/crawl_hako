# config.py
# Chứa các thông tin cấu hình dùng chung cho dự án

# ================== CẤU HÌNH API ==================
JWT_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyLCJqdGkiOiIxNWQwYjNlMi05NGEyLTRiZmYtOGExZi0zM2E0NDNkNzgzMzkiLCJpYXQiOjE3NzM3NzY3NzYsImV4cCI6MTc3NjM2ODc3Nn0.YTBkJXIgyglT4biDKsjX2KwFLmiYjAfH2Yy2lONEi8Q"
BASE_URL = "http://localhost:3000"

HEADERS = {
    "Authorization": f"Bearer {JWT_TOKEN}"
}
