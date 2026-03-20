import requests

# ===== PROXY RAW =====
raw_proxy = "45.61.96.150:6130:smyqziak:iqpff2ivwfi9"

# ===== TARGET URL =====
url = "https://docln.sbs/truyen/1028-youkoso-jitsuryoku-shijou-shugi-no-kyoushitsu-e"


def format_proxy(raw):
    ip, port, user, pwd = raw.split(":")
    return f"http://{user}:{pwd}@{ip}:{port}"


proxy_url = format_proxy(raw_proxy)

proxies = {
    "http": proxy_url,
    "https": proxy_url,
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36"
}

try:
    print("🔍 Sending request...\n")

    res = requests.get(
        url,
        proxies=proxies,
        headers=headers,
        timeout=10
    )

    print("Status:", res.status_code)
    print("Final URL:", res.url)

    # In 1000 ký tự đầu để đỡ spam
    print("\n===== RESPONSE (preview) =====\n")
    print(res.text)

except Exception as e:
    print("❌ Error:", e)