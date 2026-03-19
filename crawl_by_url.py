import argparse
import asyncio
import os
import json
import httpx
import tempfile
from pathlib import Path
from bs4 import BeautifulSoup

# Import from current BookCrawl directory
from crawl import VolumeChapterImporter
from config import BASE_URL, HEADERS
from extractors.name import extract_name
from extractors.author import extract_author
from extractors.image import extract_image
from extractors.description import extract_description
from extractors.status import extract_status
from extractors.gerners import extract_gerners

async def download_image(url: str, save_path: str) -> bool:
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, timeout=30)
            if resp.status_code == 200:
                with open(save_path, "wb") as f:
                    f.write(resp.content)
                return True
    except Exception as e:
        print(f"Lỗi tải ảnh cover: {e}")
    return False

CATEGORY_MAPPING = {
    'Action': 1, 'Adapted to Anime': 2, 'Adapted to Drama CD': 3, 'Adapted to Manga': 4,
    'Adult': 5, 'Adventure': 6, 'Age Gap': 7, 'Boys Love': 8, 'Character Growth': 9,
    'Chinese Novel': 10, 'Comedy': 11, 'Cooking': 12, 'Different Social Status': 13,
    'Drama': 14, 'Ecchi': 15, 'English Novel': 16, 'Fantasy': 17, 'Female Protagonist': 18,
    'Game': 19, 'Gender Bender': 20, 'Harem': 21, 'Historical': 22, 'Horror': 23,
    'Incest': 24, 'Isekai': 25, 'Josei': 26, 'Korean Novel': 27, 'Magic': 28,
    'Martial Arts': 29, 'Mature': 30, 'Mecha': 31, 'Military': 32, 'Misunderstanding': 33,
    'Mystery': 34, 'Netorare': 35, 'One shot': 36, 'Otome Game': 37, 'Parody': 38,
    'Psychological': 39, 'Reverse Harem': 40, 'Romance': 41, 'School Life': 42,
    'Science Fiction': 43, 'Seinen': 44, 'Shoujo': 45, 'Shoujo ai': 46, 'Shounen': 47,
    'Shounen ai': 48, 'Slice of Life': 49, 'Slow Life': 50, 'Sports': 51, 'Super Power': 52,
    'Supernatural': 53, 'Suspense': 54, 'Tragedy': 55, 'Wars': 56, 'Web Novel': 57,
    'Workplace': 58, 'Yuri': 59
}

def api_create_book(info: dict, cover_path: str) -> int | None:
    url = f"{BASE_URL}/Book/create"
    
    raw_status = str(info.get("status", "Đang tiến hành")).lower()
    status_mapped = "ongoing"
    if "hoàn thành" in raw_status or "completed" in raw_status:
        status_mapped = "completed"
    elif "tạm ngưng" in raw_status or "hidden" in raw_status:
        status_mapped = "hidden"
        
    data = [
        ("book_name",   info.get("name", "Unknown")),
        ("sub_names",   json.dumps([], ensure_ascii=False)),
        ("authors",     json.dumps([info.get("author", "Unknown")], ensure_ascii=False)),
        ("status",      status_mapped),
        ("description", info.get("description", "")),
    ]
    
    # Categories
    categories = info.get("categories", [])
    valid_cat_found = False
    for cat in categories:
        cat_id = CATEGORY_MAPPING.get(str(cat).strip())
        if cat_id is not None:
            data.append(("categories[]", str(cat_id)))
            valid_cat_found = True
            
    # Đăng ký một danh mục mặc định nếu không tag nào khớp để tránh lỗi database null
    if not valid_cat_found:
        data.append(("categories[]", "57")) # Mặc định là Web Novel (57)
        

    try:
        with open(cover_path, "rb") as img_f:
            ext = Path(cover_path).suffix or ".jpg"
            files = {"image": (f"cover{ext}", img_f, "image/jpeg")}
            
            # Use httpx or requests to upload. Using httpx sync for simplicity here or httpx Client
            import requests
            resp = requests.post(url, data=data, files=files, headers=HEADERS, timeout=60)
            
        print(f"[Create Book API] Status: {resp.status_code}")
        
        if resp.status_code not in (200, 201):
            print(f"[Create Book API] Error Response: {resp.text[:500]}")
            return None
            
        resp_json = resp.json()
        print(f"Response: {resp_json}")
        # Dựa nào backend có thể trả về { data: { book_id: ... } } hoặc { id: ... } 
        # Cần tìm book_id một cách an toàn
        data_obj = resp_json.get("data", {})
        book_id = None
        if isinstance(data_obj, dict):
            book_id = data_obj.get("book_id") or data_obj.get("id")
            
        if not book_id:
            book_id = resp_json.get("book_id") or resp_json.get("id")
            
        return book_id
        
    except Exception as e:
        print(f"[Create Book API] Exception: {e}")
        return None

async def process_custom_url(book_url: str):
    print(f"\n============================================================")
    print(f"Đang xử lý truyện từ URL: {book_url}")
    print(f"============================================================")

    # 1. Tải HTML trang truyện
    print("⏳ Đang tải thông tin trang...")
    async with httpx.AsyncClient(timeout=30) as client:
        try:
            r = await client.get(book_url, headers={"User-Agent": "Mozilla/5.0"})
            r.raise_for_status()
            soup = BeautifulSoup(r.text, 'html.parser')
        except Exception as e:
            print(f"❌ Không thể tải trang truyện: {e}")
            return

    # 2. Bóc tách dữ liệu sử dụng các modules đã xây dựng sẵn trong BookCrawl
    print("⏳ Đang bóc tách thông tin...")
    book_info = {
        "name": extract_name(soup),
        "author": extract_author(soup),
        "image_url": extract_image(soup),
        "status": extract_status(soup),
        "description": extract_description(soup),
        "categories": extract_gerners(soup)
    }

    if not book_info["name"]:
        print("❌ Không thể lấy tên truyện. URL có hợp lệ không?")
        return

    print(f"📖 Tên truyện: {book_info['name']}")
    print(f"✍️ Tác giả: {book_info['author']}")
    print(f"🏷️ Thể loại: {', '.join(book_info['categories']) if book_info['categories'] else 'Không có'}")

    # 3. Tải ảnh bìa
    cover_path = "temp_cover.jpg"
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
        cover_path = f.name
        
    if book_info["image_url"]:
        print("⏳ Đang tải ảnh bìa...")
        await download_image(book_info["image_url"], cover_path)
    else:
        print("⚠️ Không tìm thấy ảnh bìa, dùng file trống.")
        # Create an empty dummy file just so it doesn't crash if needed
        with open(cover_path, "wb") as f:
            f.write(b"")

    # 4. Tạo Sach tren server (hoc hoi crawl_stv.py)
    print("⏳ Gọi API tạo sách...")
    backend_book_id = api_create_book(book_info, cover_path)
    
    # Xoá file tmp ảnh
    if os.path.exists(cover_path):
        os.remove(cover_path)

    if not backend_book_id:
        print("❌ Tạo sách thất bại, ngưng tiến trình crawl chương.")
        return
        
    print(f"✅ Đã tạo sách thành công trên server! ID: {backend_book_id}")

    # 5. Khởi tạo VolumeChapterImporter từ file crawl.py để crawl chapters
    print("⏳ Bắt đầu crawl volumes và chapters...")
    importer = VolumeChapterImporter(backend_book_id, book_url)
    
    # Gọi hàm run() của importer (chứa việc tạo Volume, Chương và Upload Markdown)
    try:
        await importer.run()
        print(f"🎉 Hoàn thành crawl dữ liệu cho: {book_info['name']}")
    except Exception as e:
        print(f"🔥 Có lỗi xảy ra trong tiến trình lấy chương: {e}")


async def main():
    parser = argparse.ArgumentParser(description="Script tạo sách từ URL docln và tự động crawl chapters")
    parser.add_argument("--url", type=str, required=True, help="URL của truyện Docln muốn crawl")
    args = parser.parse_args()

    await process_custom_url(args.url)

if __name__ == "__main__":
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
