import csv
import os
import httpx
import asyncio
from bs4 import BeautifulSoup
from docx import Document
import re

from image import extract_image
from name import extract_name
from gerners import extract_gerners  # Typos corrected
from author import extract_author
from illustrator import extract_illustrator
from status import extract_status
from description import extract_description
from chapterInVolume import extract_chapter_in_volume
from chapterContent import extract_chapter_content

class Book:
    def __init__(self, url) -> None:
        self.url = url
        self.soup = None

    async def init(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(self.url)
        self.soup = BeautifulSoup(response.content, 'html.parser')
        return self

    async def name(self):
        return extract_name(self.soup)   

    async def image(self):
        return extract_image(self.soup)

    async def genres(self):  # Fixed typo
        return extract_gerners(self.soup)

    async def author(self):
        return extract_author(self.soup)
    
    async def illustrator(self):
        return extract_illustrator(self.soup)
    
    async def status(self):
        return extract_status(self.soup)
    
    async def description(self):
        return extract_description(self.soup)
    
    async def chapters_in_volume(self):
        return extract_chapter_in_volume(self.soup)
    
    async def fetch_and_save_chapters(self, basePostUrl):
        story_name = self.sanitize_name(await self.name())
        story_folder = os.path.join("U:/Book", story_name)
        os.makedirs(story_folder, exist_ok=True)

        volumes = await self.chapters_in_volume()

        createVoLumeUrl = basePostUrl + '/Book/Volume/create'
        createChapterUrl = basePostUrl + '/Book/Volume/Chapter/create'

        if volumes:
            volume_count = 1
            for volume_info in volumes:
                dataVolume = {
                    'book_name': await self.name(),
                    'volume_name': volume_info['volume']
                }

                async with httpx.AsyncClient() as client:
                    responseVolume = await client.post(createVoLumeUrl, data=dataVolume)

                if responseVolume.status_code == 200:
                    print('Dữ liệu đã được gửi tới volume thành công!')
                    print('Phản hồi:', responseVolume.text)

                    volume_folder = os.path.join(story_folder, self.sanitize_name(f"Volume_{volume_count} {volume_info['volume']}"))
                    os.makedirs(volume_folder, exist_ok=True)

                    chapter_count = 1
                    for chapter in volume_info["chapters"]:
                        chapter_name = chapter["chapterName"]
                        chapter_url = chapter["chapterLink"]
                        print(f"Fetching: {chapter_url}")

                        print("Delay for 10s to avoid 429 status")
                        await asyncio.sleep(10)

                        # Không sử dụng await vì extract_chapter_content không phải là hàm bất đồng bộ
                        chapter_content = extract_chapter_content(chapter_url)

                        if chapter_content:
                            chapter_file_name = self.sanitize_name(f"Chapter_{chapter_count} {chapter_name}") + ".docx"
                            chapter_file_path = os.path.join(volume_folder, chapter_file_name)
                            self.save_to_word(chapter_content, chapter_file_path)
                            print(f"Content saved to {chapter_file_path}")
                            chapter_count += 1

                            dataChapter = {
                                'book_name': await self.name(),
                                'volume_name': volume_info['volume'],
                                'chapter_name': chapter_name,
                                'content': chapter_file_path
                            }

                            async with httpx.AsyncClient() as client:
                                responseChapter = await client.post(createChapterUrl, data=dataChapter)

                            if responseChapter.status_code == 200:
                                print('Dữ liệu đã được gửi tới chapter thành công!')
                                print('Phản hồi:', responseChapter.text)
                            else:
                                print(f'Có lỗi xảy ra: {responseChapter.status_code}')

                        else:
                            print(f"No content found for {chapter_name}.")

                    volume_count += 1
                else:
                    print(f'Có lỗi xảy ra: {responseVolume.status_code}')
        else:
            print("No volumes or chapters found.")

    def save_to_word(self, text_rows, file_name):
        try:
            doc = Document()
            for paragraph in text_rows:
                doc.add_paragraph(paragraph)
            doc.save(file_name)
        except Exception as err:
            print(f"Error saving file {file_name}: {err}")

    def sanitize_name(self, name):
        return re.sub(r'[<>:"/\\|?*\.!@#$%^&*()_+=-]', '', name)  # Thay thế bằng ''

    
    async def save_to_csv(self, filename):
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'Image', 'Genres', 'Author', 'Illustrator', 'Status', 'Description'])
            writer.writerow([
                await self.name(),
                await self.image(),
                ', '.join(await self.genres()) if await self.genres() else None,
                await self.author(),
                await self.illustrator(),
                await self.status(),
                await self.description()
            ])
    
    async def save_all_to_database(self, url):
        createBookUrl = url + '/Book/create'

        dataBook = {
            'name': await self.name(),
            'image': await self.image(),
            'author': await self.author(),
            'artist': await self.illustrator(),
            'status': await self.status(),
            'decription': await self.description(),
            'categories': await self.genres()
        }

        async with httpx.AsyncClient() as client:
            responseBook = await client.post(createBookUrl, data=dataBook)

        if responseBook.status_code == 200:
            print('Dữ liệu đã được gửi tới book thành công!')
            print('Phản hồi:', responseBook.text)
        else:
            print(f'Có lỗi xảy ra: {responseBook.status_code}')

        await self.fetch_and_save_chapters(url)

# Mảng URL chứa danh sách các loại sách
urls = [
]

postURL = "http://localhost:3000"

# Tạo Semaphore với giới hạn 3
semaphore = asyncio.Semaphore(3)

async def process_book(url):
    async with semaphore:  # Chỉ cho phép tối đa 3 task đồng thời
        try:
            book = await Book(url).init()
            await book.save_all_to_database(postURL)
        except Exception as e:
            print(f"Error processing book at {url}: {e}")

async def main():
    tasks = [process_book(url) for url in urls]  # Tạo danh sách các task
    await asyncio.gather(*tasks)  # Chạy tất cả các task

# async def process_book(url):
#     try:
#         book = await Book(url).init()
#         await book.save_all_to_database(postURL)
#     except Exception as e:
#         print(f"Error processing book at {url}: {e}")

# async def main():
#     for url in urls:  # Duyệt từng URL
#         await process_book(url)  # Chạy từng task một

asyncio.run(main())
