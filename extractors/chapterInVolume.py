# chapterInVolume.py
import requests
from bs4 import BeautifulSoup

def extract_chapter_in_volume(soup):
    try:
        volumes = []
        vol_sections = soup.findAll('section', class_='volume-list at-series basic-section volume-mobile gradual-mobile')

        if vol_sections:
            for vol in vol_sections:
                volume_info = {
                    "volume": "",
                    "chapters": []
                }

                header = vol.find("header")
                if header:
                    name = header.find("span", class_="sect-title")
                    if name:
                        volume_info["volume"] = name.get_text(strip=True)
                
                chapter_divs = vol.findAll("div", class_="chapter-name")
                for chapter in chapter_divs:
                    a_tag = chapter.find('a')
                    if a_tag:
                        chapter_name = a_tag.get_text(strip=True)
                        chapter_link = a_tag['href']
                    else:
                        chapter_name = chapter.get_text(strip=True)
                        chapter_link = chapter.find('a', href=True)['href'] if chapter.find('a', href=True) else ""

                    volume_info["chapters"].append({
                        "chapterName": chapter_name,
                        "chapterLink": "https://docln.sbs" + chapter_link
                    })
                
                volumes.append(volume_info)

            return volumes
        else:
            return None
    except Exception as err:
        print("Lỗi ở đâu đó", err)
        return None

# # Send a GET request to fetch the content of the page
# response = requests.get("https://docln.sbs/truyen/259-toi-la-nhen-thi-sao")

# # Parse the content with BeautifulSoup
# soup = BeautifulSoup(response.content, 'html.parser')

# # Test the function
# test = extract_chapter_in_volume(soup)
# print(test)
