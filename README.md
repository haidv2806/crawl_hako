# BookCrawl

Dự án thu thập (crawl) dữ liệu truyện từ trang web `docln.net` / `docln.sbs` và gửi lên một API server nội bộ (ví dụ: `http://localhost:3000`).

## Yêu cầu (Requirements)

Cài đặt các thư viện cần thiết bằng pip:

```bash
pip install -r requirements.txt
```

## Các file chính

- `Book.py`: Chứa class `Book` thực hiện việc lấy thông tin truyện (tên, tác giả, mô tả, ảnh bìa, các chương/tập) từ một URL cụ thể và lưu các chương vào file `.docx` cũng như đẩy trực tiếp lên server.
- `crawl.py`: Script dùng `asyncio` và `httpx` để import dữ liệu cho một danh sách các truyện (sử dụng JWT token để xác thực với API).
- Các module con (`author.py`, `chapterContent.py`, `description.py`, `image.py`, ...): Hỗ trợ bóc tách (extract) các thành phần cụ thể của truyện từ mã nguồn HTML qua BeautifulSoup.

## Hướng dẫn sử dụng

1. **Cấu hình API gốc**:
   Kiểm tra và sửa các biến `BASE_URL`, `postURL`, và `JWT_TOKEN` trong các file `crawl.py` và `Book.py` nếu cần thiết (mặc định đang gọi đến `http://localhost:3000`).

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

## Lưu ý

- Các phiên bản Word document (.docx) sẽ được cấu hình lưu vào một thư mục cứng như `U:/Book/...` trong file `Book.py`. Hãy điều chỉnh lại đường dẫn cho phù hợp với máy của bạn.
- Khi đẩy lên Git, các thư mục môi trường ảo (ví dụ `myenv`, `pocy`) và các cache đã được tự động loại bỏ thông qua `.gitignore`.
