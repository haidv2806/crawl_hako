import time
from req_config import bypass_get

url = "https://docln.sbs/truyen/259-toi-la-nhen-thi-sao"

print("--- Testing Proxy Rotation (3 requests) ---")

for i in range(1, 4):
    print(f"\nRequest #{i}...")
    start_time = time.time()
    html = bypass_get(url)
    end_time = time.time()
    
    if html:
        print(f"SUCCESS (Length: {len(html)})")
        print(f"Time taken: {end_time - start_time:.2f}s")
        # In thử 1 đoạn HTML để check
        print("HTML Preview:", html[:200].replace('\n', ' '))
    else:
        print("FAILED")