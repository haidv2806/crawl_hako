import argparse
import asyncio
import os
from extractors.chapterContent import extract_chapter_content, save_to_markdown

async def main():
    parser = argparse.ArgumentParser(description="Crawl content of a specific chapter from docln.sbs")
    parser.add_argument("--url", type=str, required=True, help="URL of the chapter")
    parser.add_argument("--output", type=str, default="ChapterContent.md", help="Output file name (default: ChapterContent.md)")
    parser.add_argument("--print", action="store_true", help="Print content to console")
    
    args = parser.parse_args()
    
    print(f"⏳ Đang lấy nội dung từ: {args.url}...")
    content = await extract_chapter_content(args.url)
    
    if content:
        if args.print:
            print("\n".join(content))
        
        save_to_markdown(content, args.output)
        print(f"✅ Đã lưu nội dung vào file: {args.output}")
    else:
        print("❌ Không tìm thấy nội dung hoặc có lỗi xảy ra.")

if __name__ == "__main__":
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
