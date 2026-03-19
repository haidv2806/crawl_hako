import requests
import httpx
from config import FLARESOLVERR_URL, BROWSER_TIMEOUT

def bypass_get(url: str):
    """
    Đồng bộ (sync): Sử dụng requests để gọi FlareSolverr
    """
    payload = {
        "cmd": "request.get",
        "url": url,
        "maxTimeout": BROWSER_TIMEOUT
    }
    try:
        # Timeout của requests thực tế nên lớn hơn maxTimeout của FlareSolverr một chút
        response = requests.post(FLARESOLVERR_URL, json=payload, timeout=(BROWSER_TIMEOUT / 1000) + 10)
        res_json = response.json()
        if res_json.get("status") == "ok":
            return res_json["solution"]["response"]
        else:
            print(f"[Bypass] Lỗi từ FlareSolverr: {res_json.get('message')}")
    except Exception as e:
        print(f"[Bypass] Lỗi khi gọi FlareSolverr: {e}")
    return None

async def bypass_get_async(url: str):
    """
    Bất đồng bộ (async): Sử dụng httpx để gọi FlareSolverr
    """
    payload = {
        "cmd": "request.get",
        "url": url,
        "maxTimeout": BROWSER_TIMEOUT
    }
    try:
        # Timeout của httpx thực tế nên lớn hơn maxTimeout của FlareSolverr một chút
        async with httpx.AsyncClient(timeout=(BROWSER_TIMEOUT / 1000) + 10) as client:
            response = await client.post(FLARESOLVERR_URL, json=payload)
            res_json = response.json()
            if res_json.get("status") == "ok":
                return res_json["solution"]["response"]
            else:
                print(f"[Bypass] Lỗi từ FlareSolverr: {res_json.get('message')}")
    except Exception as e:
        print(f"[Bypass] Lỗi khi gọi FlareSolverr (Async): {e}")
    return None
