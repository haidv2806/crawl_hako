import requests
import httpx
import time
import asyncio
from config import FLARESOLVERR_URL, BROWSER_TIMEOUT, get_next_proxy

def bypass_get(url: str, max_retries: int = 3):
    """
    Đồng bộ (sync): Sử dụng requests để gọi FlareSolverr con retry logic
    """
    for attempt in range(max_retries):
        proxy = get_next_proxy()
        payload = {
            "cmd": "request.get",
            "url": url,
            "maxTimeout": BROWSER_TIMEOUT,
            "proxy": proxy
        }
        
        try:
            # Timeout của requests thực tế nên lớn hơn maxTimeout của FlareSolverr một chút
            response = requests.post(FLARESOLVERR_URL, json=payload, timeout=(BROWSER_TIMEOUT / 1000) + 10)
            res_json = response.json()
            
            if res_json.get("status") == "ok":
                return res_json["solution"]["response"]
            
            message = res_json.get("message", "")
            print(f"[Bypass] Lỗi từ FlareSolverr (Lần {attempt+1}): {message}")
            if proxy:
                print(f"[Bypass] Proxy used: {proxy.get('url')}")
            
            if "Cloudflare has blocked this request" in message or "IP is banned" in message:
                print("⏳ Gặp lỗi bị chặn, chờ 30s rồi thử lại với proxy tiếp theo...")
                time.sleep(30)
                continue
            else:
                # Các lỗi khác có thể không cần chờ lâu hoặc không thể fix bằng cách retry
                break
                
        except Exception as e:
            print(f"[Bypass] Lỗi kết nối FlareSolverr (Lần {attempt+1}): {e}")
            time.sleep(5)
            
    return None

async def bypass_get_async(url: str, max_retries: int = 3):
    """
    Bất đồng bộ (async): Sử dụng httpx để gọi FlareSolverr con retry logic
    """
    for attempt in range(max_retries):
        proxy = get_next_proxy()
        payload = {
            "cmd": "request.get",
            "url": url,
            "maxTimeout": BROWSER_TIMEOUT,
            "proxy": proxy
        }
        
        try:
            # Timeout của httpx thực tế nên lớn hơn maxTimeout của FlareSolverr một chút
            async with httpx.AsyncClient(timeout=(BROWSER_TIMEOUT / 1000) + 10) as client:
                response = await client.post(FLARESOLVERR_URL, json=payload)
                res_json = response.json()
                
                if res_json.get("status") == "ok":
                    return res_json["solution"]["response"]
                
                message = res_json.get("message", "")
                print(f"[Bypass] Lỗi từ FlareSolverr (Async - Lần {attempt+1}): {message}")
                if proxy:
                    print(f"[Bypass] Proxy used (Async): {proxy.get('url')}")
                
                if "Cloudflare has blocked this request" in message or "IP is banned" in message:
                    print("⏳ Gặp lỗi bị chặn, chờ 30s rồi thử lại với proxy tiếp theo...")
                    await asyncio.sleep(30)
                    continue
                else:
                    break
                    
        except Exception as e:
            print(f"[Bypass] Lỗi kết nối FlareSolverr (Async - Lần {attempt+1}): {e}")
            await asyncio.sleep(5)
            
    return None
