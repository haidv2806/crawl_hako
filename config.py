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

raw_proxies = [
    "31.59.20.176:6754:zixtfewq:e82j30zrhhpd",
    "23.95.150.145:6114:zixtfewq:e82j30zrhhpd",
    "198.23.239.134:6540:zixtfewq:e82j30zrhhpd",
    "45.38.107.97:6014:zixtfewq:e82j30zrhhpd",
    "107.172.163.27:6543:zixtfewq:e82j30zrhhpd",
    "198.105.121.200:6462:zixtfewq:e82j30zrhhpd",
    "64.137.96.74:6641:zixtfewq:e82j30zrhhpd",
    "216.10.27.159:6837:zixtfewq:e82j30zrhhpd",
    "142.111.67.146:5611:zixtfewq:e82j30zrhhpd",
    "191.96.254.138:6185:zixtfewq:e82j30zrhhpd",
]

# Parse proxies into objects
def _parse_proxy(proxy_str):
    parts = proxy_str.split(":")
    return {
        "url": f"http://{parts[0]}:{parts[1]}",
        "username": parts[2],
        "password": parts[3]
    }

PROXIES = [_parse_proxy(p) for p in raw_proxies]
_proxy_index = 0

def get_next_proxy():
    global _proxy_index
    if not PROXIES:
        return None
    proxy = PROXIES[_proxy_index]
    _proxy_index = (_proxy_index + 1) % len(PROXIES)
    return proxy
