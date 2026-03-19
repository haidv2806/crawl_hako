import csv
import os
import requests
from bs4 import BeautifulSoup
from docx import Document
import time
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
        response = requests.get(url)
        self.soup = BeautifulSoup(response.content, 'html.parser')

    def name(self):
        return extract_name(self.soup)   

    def image(self):
        return extract_image(self.soup)

    def genres(self):  # Fixed typo
        return extract_gerners(self.soup)

    def author(self):
        return extract_author(self.soup)
    
    def illustrator(self):
        return extract_illustrator(self.soup)
    
    def status(self):
        return extract_status(self.soup)
    
    def description(self):
        return extract_description(self.soup)
    
    def chapters_in_volume(self):
        return extract_chapter_in_volume(self.soup)
    
    def fetch_and_save_chapters(self, basePostUrl):
        # response = requests.get(url)
        # soup = BeautifulSoup(response.content, 'html.parser')

        story_name = self.sanitize_name(extract_name(self.soup))
        # lưu dữ liệu vào 1 đường dẫn cụ thể
        story_folder = os.path.join("U:/Book", story_name)

        os.makedirs(story_folder, exist_ok=True)

        volumes = extract_chapter_in_volume(self.soup)

        createVoLumeUrl = basePostUrl + '/Book/Volume/create'
        createChapterUrl = basePostUrl + '/Book/Volume/Chapter/create'

        if volumes:
            volume_count = 1
            for volume_info in volumes:

                dataVolume = {
                    'book_name': self.name(),
                    'volume_name': volume_info['volume']
                }

                # Gửi yêu cầu POST
                responseVolume = requests.post(createVoLumeUrl, data=dataVolume)

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
                        time.sleep(10)

                        chapter_content = extract_chapter_content(chapter_url)

                        if chapter_content:
                            chapter_file_name = self.sanitize_name(f"Chapter_{chapter_count} {chapter_name}") + ".docx"
                            chapter_file_path = os.path.join(volume_folder, chapter_file_name)
                            self.save_to_word(chapter_content, chapter_file_path)
                            print(f"Content saved to {chapter_file_path}")
                            chapter_count += 1

                            # # Chuyển đổi đường dẫn từ U:/Book/... sang /book/...
                            # relative_path = chapter_file_path.replace("U:\Book", "\Book")

                            dataChapter = {
                                'book_name': self.name(),
                                'volume_name': volume_info['volume'],
                                'chapter_name': chapter_name,
                                'content': chapter_file_path
                            }

                            # Gửi yêu cầu POST
                            responseChapter = requests.post(createChapterUrl, data=dataChapter)

                            # Kiểm tra phản hồi từ server
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
        return re.sub(r'[<>:"/\\|?*\.]', ' ', name)
    
    def save_to_csv(self, filename):
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'Image', 'Genres', 'Author', 'Illustrator', 'Status', 'Description'])
            writer.writerow([
                self.name(),
                self.image(),
                ', '.join(self.genres()) if self.genres() else None,
                self.author(),
                self.illustrator(),
                self.status(),
                self.description()
            ])
    
    def save_all_to_database(self, url):
        createBookUrl = url + '/Book/create'

        # Dữ liệu cần gửi
        dataBook = {
            'name': self.name(),
            'image': self.image(),
            'author': self.author(),
            'artist': self.illustrator(),
            'status': self.status(),
            'decription': self.description(),
            'categories': self.genres()
        }

        

        # Gửi yêu cầu POST
        responseBook = requests.post(createBookUrl, data=dataBook)

        # Kiểm tra phản hồi từ server
        if responseBook.status_code == 200:
            print('Dữ liệu đã được gửi tới book thành công!')
            print('Phản hồi:', responseBook.text)
        else:
            print(f'Có lỗi xảy ra: {responseBook.status_code}')

        self.fetch_and_save_chapters(url)


url = "https://docln.net/truyen/259-toi-la-nhen-thi-sao"
postURL = "http://localhost:3000"
book = Book(url)

# Gửi tất cả dữ liệu về cuốn sách, các tập, và chương tới API localhost
book.save_all_to_database(postURL)