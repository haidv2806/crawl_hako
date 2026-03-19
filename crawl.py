# importer.py
import asyncio
import os
import re
import json
import httpx
from bs4 import BeautifulSoup

# DÙNG ĐÚNG HÀM CỦA BẠN
from extractors.chapterInVolume import extract_chapter_in_volume
from extractors.chapterContent import extract_chapter_content   

# ================== CẤU HÌNH ==================
from config import BASE_URL, HEADERS, JWT_TOKEN

# (book_id, url_truyện)
JOBS = [
    (5, "https://docln.sbs/truyen/1879-kuma-kuma-kuma-bear"),
    (6, "https://docln.sbs/truyen/5442-trash-of-the-counts-family"),
    (7, "https://docln.sbs/truyen/8997-nageki-no-bourei-wa-intai-shitai-saijiyaku-hanta-ni-yoru-saikiyou-patei-ikusei-jutsu"),
    (8, "https://docln.sbs/truyen/8960-im-the-evil-lord-of-an-intergalactic-empire"),
    (9, "https://docln.sbs/truyen/3311-nhan-vat-phu-tieu-thuyet"),
    (10, "https://docln.sbs/truyen/447-reincarnated-as-a-dragons-egg-lets-aim-to-be-the-strongest"),
    (11, "https://docln.sbs/truyen/219-dieu-hanh-tu-than-den-the-gioi-song-song"),
    (12, "https://docln.sbs/truyen/16466-throne-of-magical-arcana"),
    (13, "https://docln.sbs/truyen/11586-shimotsuki-wa-mob-ga-suki"),
    (14, "https://docln.sbs/truyen/787-tensei-shitara-kendeshita"),
    (15, "https://docln.sbs/truyen/767-arifureta-shokugyou-de-sekai-saikyou"),
    (16, "https://docln.sbs/truyen/4981-otonari-no-tenshi-sama-ni-itsu-no-aida-ni-ka-dame-ningen-ni-sareteiru-ken"),
    (17, "https://docln.sbs/truyen/214-konjiki-no-word-master"),
]

# ======================================================
class VolumeChapterImporter:
    def __init__(self, book_id: int, novel_url: str):
        self.book_id = book_id
        self.novel_url = novel_url
        self.soup = None

    async def init(self):
        async with httpx.AsyncClient(timeout=30) as client:
            headers = {"User-Agent": "Mozilla/5.0"}
            r = await client.get(self.novel_url, headers=headers)
            r.raise_for_status()
            self.soup = BeautifulSoup(r.text, 'html.parser')
        return self

    def sanitize(self, text: str) -> str:
        return re.sub(r'[<>:"/\\|?*\x00-\x1F]', '', text).strip()

    async def create_volume(self, volume_name: str):
        url = f"{BASE_URL}/Book/Volume/create"
        payload = {
            "book_id": self.book_id,
            "volume_name": volume_name,
            "status": "completed"
        }
        
        async with httpx.AsyncClient() as client:
            try:
                r = await client.post(url, json=payload, headers=HEADERS, timeout=30)
                
                if r.status_code not in (200, 201):
                    print(f"❌ Tạo volume thất bại: {r.status_code} | {r.text}")
                    return None
                
                res_json = r.json()
                
                # Logic lấy ID (đã fix ở bước trước)
                data_obj = res_json.get("data")
                vid = None
                if data_obj and isinstance(data_obj, dict):
                    vid = data_obj.get("volume_id")
                if not vid:
                    vid = res_json.get("volume_id") or res_json.get("id")

                if not vid:
                    print(f"❌ Không lấy được volume_id. Response gốc: {res_json}")
                    return None
                    
                print(f"✅ Đã tạo volume: {volume_name} (ID: {vid})")
                return vid

            except Exception as e:
                print(f"❌ Lỗi connection volume: {e}")
                return None

    async def create_chapter(self, client: httpx.AsyncClient, volume_id: int, chapter_name: str, content_lines: list):
        url = f"{BASE_URL}/Book/Volume/Chapter/create"
        safe_name = self.sanitize(chapter_name)[:50]
        temp_md = f"temp_{safe_name}.md"

        markdown_text = "\n\n".join(filter(None, content_lines))
        with open(temp_md, "w", encoding="utf-8") as f:
            f.write(markdown_text)

        # --- FIX LỖI "notes phải là mảng" ---
        # 1. Không dùng json.dumps (vì nó biến thành string).
        # 2. Dùng key "notes[]" để ép Node.js nhận diện là Array khi chỉ có 1 phần tử.
        data = {
            "volume_id": str(volume_id),
            "chapter_name": chapter_name,
            "status": "completed",
            "notes[]": "Import tự động từ docln.sbs" 
        }

        files = {
            "markdownFile": (f"{safe_name}.md", open(temp_md, "rb"), "text/markdown")
        }

        try:
            r = await client.post(url, data=data, files=files, headers=HEADERS, timeout=120)
            
            if r.status_code in (200, 201):
                print(f"  ✅ Upload thành công: {chapter_name}")
            else:
                print(f"  ❌ Thất bại: {chapter_name} | Status: {r.status_code}")
                # In chi tiết lỗi để debug
                print(f"  Response: {r.text[:500]}") 
        except Exception as e:
            print(f"  ❌ Lỗi upload chapter: {chapter_name} → {e}")
        finally:
            files["markdownFile"][1].close()
            try:
                os.remove(temp_md)
            except:
                pass

    async def run(self):
        await self.init()
        volumes = extract_chapter_in_volume(self.soup)
        
        if not volumes:
            print("⚠️ Không lấy được danh sách chapter!")
            return

        print(f"📂 Tìm thấy {len(volumes)} volume trong truyện ID {self.book_id}")

        async with httpx.AsyncClient(timeout=120) as client:
            for vol in volumes:
                vol_name = self.sanitize(vol.get("volume", "") or "Tập chính")
                
                volume_id = await self.create_volume(vol_name)
                if not volume_id:
                    print(f"⏩ Bỏ qua các chapter của volume '{vol_name}' do lỗi tạo volume.")
                    continue

                for chap in vol["chapters"]:
                    name = chap["chapterName"]
                    url = chap["chapterLink"]

                    print(f"  ⬇️ Đang crawl: {name}")
                    
                    await asyncio.sleep(6) 

                    lines = extract_chapter_content(url)
                    if lines is None or len(lines) == 0:
                        print(f"  ⚠️ Bỏ qua (trống): {name}")
                        continue

                    await self.create_chapter(client, volume_id, name, lines)

        print(f"🏁 HOÀN TẤT import book_id = {self.book_id}")


# ======================= CHẠY =======================
semaphore = asyncio.Semaphore(2)

async def process(book_id, url):
    async with semaphore:
        importer = VolumeChapterImporter(book_id, url)
        try:
            await importer.run()
        except Exception as e:
            print(f"🔥 Lỗi Fatal cho truyện {book_id}: {e}")

async def main():
    if not JOBS:
        print("Không có job nào.")
        return
    
    tasks = [process(bid, url) for bid, url in JOBS]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
    asyncio.run(main())