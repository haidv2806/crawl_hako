# config.py
# Chứa các thông tin cấu hình dùng chung cho dự án

import json
from pathlib import Path

# ================== CẤU HÌNH API ==================
JWT_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjozOSwianRpIjoiMGNkNTlmZWUtNWEwZC00OWFmLTk5OGEtNTljYmNmYTVjYmVjIiwiaWF0IjoxNzc1Mzk4MDY0LCJleHAiOjE3Nzc5OTAwNjR9.pWbRf_amiQitIvyoWlu_G2BW42Z8cL989WSvoqpWXTs"
# BASE_URL = "http://localhost:3000"
BASE_URL = "https://e-books.info.vn"

# ================== CẤU HÌNH BYPASS ==================
FLARESOLVERR_URL = "http://localhost:8191/v1"
BROWSER_TIMEOUT = 120000 # 2 phút

# ================== CẤU HÌNH SKIP URLs ==================
SKIP_URLS_FILE = Path(__file__).parent / "skip_urls.json"
_skip_urls = set()

HEADERS = {
    "Authorization": f"Bearer {JWT_TOKEN}"
}

raw_proxies = [
    "45.61.96.150:6130:smyqziak:iqpff2ivwfi9",
    "64.137.121.71:6326:smyqziak:iqpff2ivwfi9",
    "82.24.236.90:7900:smyqziak:iqpff2ivwfi9",
    "45.159.53.38:7410:smyqziak:iqpff2ivwfi9",
    "154.6.121.19:5986:smyqziak:iqpff2ivwfi9",
    "45.61.96.117:6097:smyqziak:iqpff2ivwfi9",
    "45.38.67.11:6943:smyqziak:iqpff2ivwfi9",
    "31.58.19.223:6495:smyqziak:iqpff2ivwfi9",
    "45.39.50.245:6663:smyqziak:iqpff2ivwfi9",
    "45.147.187.69:6442:smyqziak:iqpff2ivwfi9",
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

# ==================== SKIP URLs MANAGEMENT ====================
def _load_skip_urls():
    """Load skip URLs from file"""
    global _skip_urls
    if SKIP_URLS_FILE.exists():
        try:
            with open(SKIP_URLS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                _skip_urls = set(data.get('urls', []))
        except Exception as e:
            print(f"⚠️ Error loading skip_urls.json: {e}")
            _skip_urls = set()
    else:
        _skip_urls = set()

def _save_skip_urls():
    """Save skip URLs to file"""
    try:
        with open(SKIP_URLS_FILE, 'w', encoding='utf-8') as f:
            json.dump({
                'urls': sorted(list(_skip_urls)),
                'count': len(_skip_urls)
            }, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"⚠️ Error saving skip_urls.json: {e}")

def should_skip_url(url: str) -> bool:
    """Check if URL should be skipped"""
    global _skip_urls
    if not _skip_urls:
        _load_skip_urls()
    return url in _skip_urls

def add_skip_url(url: str):
    """Add URL to skip list"""
    global _skip_urls
    if not _skip_urls:
        _load_skip_urls()
    
    if url not in _skip_urls:
        _skip_urls.add(url)
        _save_skip_urls()
        print(f"✅ Added to skip list: {url}")
    else:
        print(f"ℹ️ Already in skip list: {url}")

def add_skip_urls_batch(urls: list):
    """Add multiple URLs to skip list"""
    global _skip_urls
    if not _skip_urls:
        _load_skip_urls()
    
    added = []
    for url in urls:
        if url not in _skip_urls:
            _skip_urls.add(url)
            added.append(url)
    
    if added:
        _save_skip_urls()
        print(f"✅ Added {len(added)} URLs to skip list")
    
    return len(added)

def get_skip_urls_count() -> int:
    """Get count of skip URLs"""
    global _skip_urls
    if not _skip_urls:
        _load_skip_urls()
    return len(_skip_urls)

def print_skip_urls_stats():
    """Print skip URLs statistics"""
    global _skip_urls
    if not _skip_urls:
        _load_skip_urls()
    
    print("\n" + "="*60)
    print("📋 SKIP URLs STATISTICS")
    print("="*60)
    print(f"Total skipped URLs: {len(_skip_urls)}")
    
    if _skip_urls and len(_skip_urls) <= 10:
        print("\nSkipped URLs:")
        for url in sorted(list(_skip_urls)):
            print(f"  - {url}")
    elif _skip_urls:
        print("\nFirst 10 skipped URLs:")
        for url in sorted(list(_skip_urls))[:10]:
            print(f"  - {url}")
        print(f"  ... and {len(_skip_urls) - 10} more")
    
    print("="*60 + "\n")

# Load skip URLs on startup
_load_skip_urls()
