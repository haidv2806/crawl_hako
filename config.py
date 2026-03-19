# config.py
# Chứa các thông tin cấu hình dùng chung cho dự án

# ================== CẤU HÌNH API ==================
JWT_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyLCJqdGkiOiI0MmRjZDQ2OC1lMTQ1LTQwY2MtOWZiNy03YzFjNTNlZjEzNGUiLCJpYXQiOjE3NzM5MTc5NTAsImV4cCI6MTc3NjUwOTk1MH0.1bGYi2wxzYxqSkrPdtRSHoHiaPNTlhl-xUXPWhz-7z4"
BASE_URL = "http://localhost:3000"
# BASE_URL = "https://e-books.info.vn"

# ================== CẤU HÌNH BYPASS ==================
FLARESOLVERR_URL = "http://localhost:8191/v1"
BROWSER_TIMEOUT = 60000 # 1 phút

HEADERS = {
    "Authorization": f"Bearer {JWT_TOKEN}"
}
