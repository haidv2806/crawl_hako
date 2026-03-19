import requests
from bs4 import BeautifulSoup


def extract_chapter (soup):
    try:
        volume = []
        vol = soup.findAll('section', class_='volume-list at-series basic-section volume-mobile gradual-mobile')

        # Iterate over each volume section to find chapter names
        for volume in vol:
                header = volume.find("header")
                name = header.find("span", class_="sect-title")
                volumeName = name.contents[0].strip()
                volume.append(volumeName)
            # name = volume.findAll("div", class_="chapter-name")
            # for chapter in name:
            #     chapter_name = chapter.get_text(strip=True)
            #     print(chapter_name)
        # if name:
        #     for name in name:
        #         # header = vol.find("li")
        #         # print (header)
        #         # name = vol.findAll("div", class_="chapter-name")
        #         chaptername = name.find("a")
        #         volumeName = chaptername.contents[0].strip()
        #         volume.append(volumeName)

        #     return volume
        # else:
        #     return None
    except Exception as err:
        print("Lỗi ở đâu đó" , err)
        return None

