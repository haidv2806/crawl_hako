import asyncio
import os
import httpx
import argparse
from bs4 import BeautifulSoup
from crawl_by_url import process_custom_url
from req_config import bypass_get_async
from config import should_skip_url, add_skip_url, print_skip_urls_stats

async def crawl_page(base_url, start_page, end_page):
    # Cào 3 truyện 1 lần
    semaphore = asyncio.Semaphore(1)
    
    async def process_with_semaphore(book_url):
        async with semaphore:
            await process_custom_url(book_url)

    for page in range(start_page, end_page + 1):
        # Nối page param
        if "page=" in base_url:
            import re
            page_url = re.sub(r'page=\d+', f'page={page}', base_url)
        else:
            page_url = f"{base_url}&page={page}" if "?" in base_url else f"{base_url}?page={page}"
            
        print(f"\n📂 Đang quét trang (Bypass): {page_url}")
        
        max_retries = 3
        html = None
        for attempt in range(max_retries):
            try:
                html = await bypass_get_async(page_url)
                if html:
                    break
                print(f"⏳ Thử lại lần {attempt + 1}...")
                await asyncio.sleep(5)
            except Exception as e:
                print(f"❌ Lỗi tải trang danh sách: {e}")
                break
        
        if not html:
            print("❌ Không lấy được HTML hợp lệ, bỏ qua trang.")
            continue
            
        soup = BeautifulSoup(html, 'html.parser')
        # Lấy danh sách phần tử div có class thumb_attr series-title
        series_titles = soup.find_all('div', class_='thumb_attr series-title')
        book_urls = []
        
        for st in series_titles:
            a_tag = st.find('a')
            if a_tag and a_tag.get('href'):
                href = a_tag['href']
                full_url = href if href.startswith("http") else "https://docln.sbs" + href
                
                # Kiểm tra xem URL đã được xử lý chưa
                if should_skip_url(full_url):
                    print(f"⏭️ Bỏ qua (đã xử lý): {full_url}")
                else:
                    book_urls.append(full_url)
        
        if not book_urls:
            print("⚠️ Không tìm thấy truyện mới trên trang này. Có thể đã hết trang hoặc tất cả đã được xử lý.")
            break
            
        print(f"📚 Tìm thấy {len(book_urls)} truyện chưa xử lý trên trang {page}. Bắt đầu cào...")
        
        async def process_wrapper(url):
            """Wrapper để thêm URL vào skip list sau khi xử lý"""
            try:
                await process_with_semaphore(url)
                # Thêm vào skip list sau khi xử lý thành công
                add_skip_url(url)
            except Exception as e:
                print(f"❌ Lỗi xử lý URL {url}: {e}")
        
        tasks = [process_wrapper(url) for url in book_urls]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script quét danh sách truyện docln.sbs theo trang")
    parser.add_argument("--url", type=str, required=True, help="Base URL của trang danh sách (ví dụ: https://docln.sbs/danh-sach?truyendich=1&sapxep=top)")
    parser.add_argument("--start", type=int, default=1, help="Trang bắt đầu")
    parser.add_argument("--end", type=int, default=1, help="Trang kết thúc")
    args = parser.parse_args()
    
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    asyncio.run(crawl_page(args.url, args.start, args.end))
    
    # In thống kê skip URLs
    print_skip_urls_stats()
