# BookCrawl

Dự án thu thập (crawl) dữ liệu truyện từ trang web `docln.net` / `docln.sbs` và gửi lên một API server nội bộ (ví dụ: `http://localhost:3000`).

## Yêu cầu (Requirements)

Cài đặt các thư viện cần thiết bằng pip:

```bash
pip install -r requirements.txt
```

## Các file chính

- `Book.py`: Chứa class `Book` thực hiện việc lấy thông tin truyện (tên, tác giả, mô tả, ảnh bìa, các chương/tập) từ một URL cụ thể và lưu các chương vào file `.docx` cũng như đẩy trực tiếp lên server.
- `crawl.py`: Script dùng `asyncio` và `httpx` để import dữ liệu cho một danh sách các truyện.
- `config.py`: Tệp chứa các cấu hình chung lặp lại (ví dụ JWT Token, Server URL).
- Thư mục `extractors/` (chứa các module con như `author.py`, `chapterContent.py`, `description.py`, `image.py`, ...): Hỗ trợ bóc tách (extract) các thành phần cụ thể của truyện từ mã nguồn HTML qua BeautifulSoup.

## Hướng dẫn sử dụng

# Tạo và kích hoạt virtual environment
python -m venv myenv
myenv\Scripts\activate      # Windows

1. **Cấu hình API gốc**:
   Kiểm tra và sửa các biến `BASE_URL`, `JWT_TOKEN` trong file `config.py` nếu cần thiết (mặc định đang gọi đến `http://localhost:3000`).

2. **Chạy module cơ bản (lấy 1 truyện)**:
   Mở và sửa file `Book.py` (ở cuối file) để đặt link truyện cần lấy, sau đó chạy:
   ```bash
   python Book.py
   ```

3. **Chạy module crawl hàng loạt (bất đồng bộ - async)**:
   Mở file `crawl.py` và sửa danh sách `JOBS` phù hợp với các ID và URL bạn muốn lấy. Sau đó chạy:
   ```bash
   python crawl.py
   ```

4. **Chạy module crawl theo trang (bất đồng bộ - async)**:
   Mở file `crawl_page.py` và sửa tham số `--url`, `--start`, `--end` phù hợp với nhu cầu. Sau đó chạy:
   ```bash
   python crawl_page.py --url "https://docln.sbs/danh-sach?truyendich=1&sapxep=top" --start 1 --end 10
   ```

## Lưu ý

- Các phiên bản Word document (.docx) sẽ được cấu hình lưu vào một thư mục cứng như `U:/Book/...` trong file `Book.py`. Hãy điều chỉnh lại đường dẫn cho phù hợp với máy của bạn.
- Khi đẩy lên Git, các thư mục môi trường ảo (ví dụ `myenv`, `pocy`) và các cache đã được tự động loại bỏ thông qua `.gitignore`.
