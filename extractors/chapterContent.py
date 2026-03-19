# chapterContent.py
import requests
from bs4 import BeautifulSoup
from req_config import bypass_get

def extract_chapter_content(chapter_url):
    """
    Giữ nguyên 100% logic cũ:
    - Tìm div có class "long-text no-select text-justify"
    - Với mỗi <p>:
        • nếu có <img> → lấy src của ảnh
        • nếu không có → lấy text
    """
    try:
        html = bypass_get(chapter_url)
        if not html:
            return None
            
        soup = BeautifulSoup(html, 'html.parser')
        text_rows = []
        textBox = soup.find('div', class_="long-text no-select text-justify")
        
        if textBox:
            paragraphs = textBox.findAll('p')
            for paragraph in paragraphs:
                img_tag = paragraph.find('img')
                if img_tag:
                    continue
                else:                                    # không có ảnh → lấy text
                    text_rows.append(paragraph.get_text(strip=True))
            return text_rows
        else:
            print("Text box not found in the page.")
            return None
    except requests.exceptions.RequestException as req_err:
        print(f"Request error: {req_err}")
        return None
    except Exception as err:
        print(f"Error fetching chapter content from {chapter_url}: {err}")
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