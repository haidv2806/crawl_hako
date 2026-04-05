import requests
from bs4 import BeautifulSoup


def extract_illustrator(soup):
    try:
        # Tìm tất cả các div có class 'info-item'
        info_items = soup.find_all('div', class_='info-item')
        
        for item in info_items:
            name_span = item.find('span', class_='info-name')
            if name_span and 'Họa sĩ:' in name_span.get_text():
                value_span = item.find('span', class_='info-value')
                if value_span:
                    # Lấy text từ thẻ 'a' nếu có, không thì lấy trực tiếp từ value_span
                    a_tag = value_span.find('a')
                    if a_tag:
                        return a_tag.get_text().strip()
                    return value_span.get_text().strip()
        
        print("no illustrator found")
        return None
    except Exception as err:
        print("Lỗi ở extract_illustrator:", err)
        return None
