import requests
from bs4 import BeautifulSoup


def extract_volume (soup):
    try:
        volume = []
        vol = soup.findAll('section', class_='volume-list at-series basic-section volume-mobile gradual-mobile')

        if vol:
            for vol in vol:
                header = vol.find("header")
                name = header.find("span", class_="sect-title")
                volumeName = name.contents[0].strip()
                volume.append(volumeName)

            return volume
        else:
            return None
    except Exception as err:
        print("Lỗi ở đâu đó" , err)
        return None

# # Send a GET request to fetch the content of the page
# response = requests.get("https://docln.net/truyen/259-toi-la-nhen-thi-sao")

# # Parse the content with BeautifulSoup
# soup = BeautifulSoup(response.content, 'html.parser')

# test = extract_volume(soup)
# print(test)