# config.py
# Chứa các thông tin cấu hình dùng chung cho dự án

# ================== CẤU HÌNH API ==================
JWT_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyLCJqdGkiOiI3MzYyOTQ1My1kNWNkLTRhY2EtOWIxOC1hOGFiODZlYmE5MGMiLCJpYXQiOjE3NzM5NDg5MTIsImV4cCI6MTc3NjU0MDkxMn0.5fneRW3udySHM3nN9fkQ4k7gocmzJ3WbJNpbJdYEzwU"
BASE_URL = "http://localhost:3000"
# BASE_URL = "https://e-books.info.vn"

# ================== CẤU HÌNH BYPASS ==================
FLARESOLVERR_URL = "http://localhost:8191/v1"
BROWSER_TIMEOUT = 60000 # 1 phút

HEADERS = {
    "Authorization": f"Bearer {JWT_TOKEN}"
}

raw_proxies = [

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
