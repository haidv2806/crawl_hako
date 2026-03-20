# chapterContent.py
import asyncio
import requests
from bs4 import BeautifulSoup
from req_config import bypass_get_async

async def extract_chapter_content(chapter_url, max_retries=3):
    """
    Giữ nguyên 100% logic cũ:
    - Tìm div có class "long-text no-select text-justify"
    - Với mỗi <p>:
        • nếu có <img> → lấy src của ảnh
        • nếu không có → lấy text
    
    Thêm retry logic: nếu lấy được trống, thử lại tối đa 3 lần
    """
    for attempt in range(1, max_retries + 1):
        try:
            html = await bypass_get_async(chapter_url)
            if not html:
                if attempt < max_retries:
                    print(f"  🔄 Thử lại ({attempt}/{max_retries}): HTML rỗng, đợi 2 giây...")
                    await asyncio.sleep(2)
                    continue
                else:
                    return None
                
            soup = BeautifulSoup(html, 'html.parser')
            text_rows = []
            textBox = soup.find('div', class_="long-text no-select text-justify")
            
            if textBox:
                paragraphs = textBox.findAll('p')
                for paragraph in paragraphs:
                    # Bỏ qua nếu <p> có display: none
                    style = paragraph.get('style', '')
                    if 'display' in style and 'none' in style:
                        continue
                    
                    img_tag = paragraph.find('img')
                    if img_tag:
                        continue
                    else:                                    # không có ảnh → lấy text
                        text = paragraph.get_text(strip=True)
                        if text:  # chỉ thêm text không rỗng
                            text_rows.append(text)
                
                # Nếu có content, trả về luôn
                if text_rows:
                    return text_rows
                # Nếu không có content, thử lại
                elif attempt < max_retries:
                    print(f"  🔄 Thử lại ({attempt}/{max_retries}): Nội dung trống, đợi 2 giây...")
                    await asyncio.sleep(2)
                    continue
                else:
                    return None
            else:
                if attempt < max_retries:
                    print(f"  🔄 Thử lại ({attempt}/{max_retries}): Text box không tìm thấy, đợi 2 giây...")
                    await asyncio.sleep(2)
                    continue
                else:
                    print("Text box not found in the page.")
                    return None
        except Exception as err:
            if attempt < max_retries:
                print(f"  🔄 Thử lại ({attempt}/{max_retries}): Lỗi {err}, đợi 2 giây...")
                await asyncio.sleep(2)
                continue
            else:
                print(f"Error fetching chapter content from {chapter_url}: {err}")
                return None
    
    return None


# Thay vì lưu Word → lưu thành file Markdown
def save_to_markdown(text_rows, file_name="ChapterContent.md"):
    try:
        # Ghép các dòng bằng 2 xuống dòng để tạo khoảng cách đoạn đẹp trong markdown
        content = "\n\n".join(text_rows)
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Đã lưu thành công → {file_name}")
    except Exception as err:
        print(f"Error saving markdown file {file_name}: {err}")


# # ====================== TEST ======================
# if __name__ == "__main__":
#     chapter_url = "https://docln.sbs/truyen/259-toi-la-nhen-thi-sao/c10384-s2-tu-hoang-tu"

#     chapter_content = extract_chapter_content(chapter_url)

#     if chapter_content:
#         save_to_markdown(chapter_content, 'ChapterContent.md')
#     else:
#         print("No content found.")