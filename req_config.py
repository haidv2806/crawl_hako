import requests
import httpx
import time
import asyncio
from config import FLARESOLVERR_URL, BROWSER_TIMEOUT, get_next_proxy

# ================== SESSION MANAGEMENT ==================
# Lưu session ID cho mỗi proxy: {"proxy_url": "session_id"}
proxy_sessions = {}

def create_session(proxy):
    """
    Tạo session mới cho proxy
    """
    payload = {
        "cmd": "sessions.create",
        "proxy": proxy
    }
    
    try:
        response = requests.post(
            FLARESOLVERR_URL,
            json=payload,
            timeout=30
        )
        res_json = response.json()
        
        if res_json.get("status") == "ok":
            session_id = res_json.get("session")
            proxy_url = proxy.get("url") if proxy else "direct"
            proxy_sessions[proxy_url] = session_id
            print(f"✅ Created session: {session_id} for proxy {proxy_url}")
            return session_id
        else:
            print(f"❌ Failed to create session: {res_json.get('message')}")
            return None
    except Exception as e:
        print(f"❌ Error creating session: {e}")
        return None

def destroy_session(proxy):
    """
    Xóa session của proxy
    """
    proxy_url = proxy.get("url") if proxy else "direct"
    session_id = proxy_sessions.get(proxy_url)
    
    if not session_id:
        return
    
    payload = {
        "cmd": "sessions.destroy",
        "session": session_id
    }
    
    try:
        response = requests.post(
            FLARESOLVERR_URL,
            json=payload,
            timeout=10
        )
        res_json = response.json()
        
        if res_json.get("status") == "ok":
            del proxy_sessions[proxy_url]
            print(f"✅ Destroyed session: {session_id}")
            return True
        else:
            print(f"❌ Failed to destroy session: {res_json.get('message')}")
            return False
    except Exception as e:
        print(f"❌ Error destroying session: {e}")
        return False

def get_or_create_session(proxy):
    """
    Lấy session hiện có hoặc tạo mới nếu chưa có
    """
    proxy_url = proxy.get("url") if proxy else "direct"
    
    if proxy_url in proxy_sessions:
        return proxy_sessions[proxy_url]
    
    return create_session(proxy)

def bypass_get(url: str, max_retries: int = 3):
    """
    Sync: Sử dụng session cho proxy, retry nếu fail, xóa session nếu bị block
    """
    # --- Thử với proxy + session ---
    for attempt in range(max_retries):
        proxy = get_next_proxy()
        session_id = get_or_create_session(proxy)
        
        payload = {
            "cmd": "request.get",
            "url": url,
            "maxTimeout": BROWSER_TIMEOUT,
            "session": session_id,
            "proxy": proxy
        }

        try:
            response = requests.post(
                FLARESOLVERR_URL,
                json=payload,
                timeout=(BROWSER_TIMEOUT / 1000) + 10
            )
            res_json = response.json()

            if res_json.get("status") == "ok":
                return res_json["solution"]["response"]

            message = res_json.get("message", "")
            print(f"[Bypass] Lỗi (Lần {attempt+1}): {message}")

            if proxy:
                print(f"[Bypass] Proxy used: {proxy.get('url')}")

            # Nếu bị block, xóa session cũ
            if "Cloudflare has blocked this request" in message or "IP is banned" in message:
                print(f"⚠️ Proxy bị block, xóa session và tạo lại...")
                destroy_session(proxy)
                print("⏳ Chờ 30s trước khi retry...")
                time.sleep(30)
                continue
            else:
                break

        except Exception as e:
            print(f"[Bypass] Lỗi kết nối (Lần {attempt+1}): {e}")
            time.sleep(5)

    # --- FALLBACK: dùng IP thật (không proxy) ---
    print("[Bypass] ⚠️ Thử lại bằng IP máy thật (không proxy)...")
    
    session_id = get_or_create_session(None)
    payload = {
        "cmd": "request.get",
        "url": url,
        "maxTimeout": BROWSER_TIMEOUT,
        "session": session_id
    }

    try:
        response = requests.post(
            FLARESOLVERR_URL,
            json=payload,
            timeout=(BROWSER_TIMEOUT / 1000) + 10
        )
        res_json = response.json()

        if res_json.get("status") == "ok":
            return res_json["solution"]["response"]

        print(f"[Bypass] ❌ Fallback cũng fail: {res_json.get('message')}")

    except Exception as e:
        print(f"[Bypass] ❌ Lỗi fallback: {e}")

    return None

async def bypass_get_async(url: str, max_retries: int = 3):
    """
    Async: Sử dụng session cho proxy, retry nếu fail, xóa session nếu bị block
    """
    # --- Thử với proxy + session ---
    for attempt in range(max_retries):
        proxy = get_next_proxy()
        session_id = get_or_create_session(proxy)
        
        payload = {
            "cmd": "request.get",
            "url": url,
            "maxTimeout": BROWSER_TIMEOUT,
            "session": session_id,
            "proxy": proxy
        }

        try:
            async with httpx.AsyncClient(timeout=(BROWSER_TIMEOUT / 1000) + 10) as client:
                response = await client.post(FLARESOLVERR_URL, json=payload)
                res_json = response.json()

                if res_json.get("status") == "ok":
                    return res_json["solution"]["response"]

                message = res_json.get("message", "")
                print(f"[Bypass] Lỗi Async (Lần {attempt+1}): {message}")

                if proxy:
                    print(f"[Bypass] Proxy used: {proxy.get('url')}")

                # Nếu bị block, xóa session cũ
                if "Cloudflare has blocked this request" in message or "IP is banned" in message:
                    print(f"⚠️ Proxy bị block, xóa session và tạo lại...")
                    destroy_session(proxy)
                    print("⏳ Chờ 30s trước khi retry...")
                    await asyncio.sleep(30)
                    continue
                else:
                    break

        except Exception as e:
            print(f"[Bypass] Lỗi kết nối Async (Lần {attempt+1}): {e}")
            await asyncio.sleep(5)

    # --- FALLBACK ---
    print("[Bypass] ⚠️ Async fallback về IP máy thật...")
    
    session_id = get_or_create_session(None)
    payload = {
        "cmd": "request.get",
        "url": url,
        "maxTimeout": BROWSER_TIMEOUT,
        "session": session_id
    }

    try:
        async with httpx.AsyncClient(timeout=(BROWSER_TIMEOUT / 1000) + 10) as client:
            response = await client.post(FLARESOLVERR_URL, json=payload)
            res_json = response.json()

            if res_json.get("status") == "ok":
                return res_json["solution"]["response"]

            print(f"[Bypass] ❌ Async fallback fail: {res_json.get('message')}")

    except Exception as e:
        print(f"[Bypass] ❌ Async fallback lỗi: {e}")

    return None
