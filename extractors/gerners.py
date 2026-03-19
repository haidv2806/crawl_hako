import requests
from bs4 import BeautifulSoup


def extract_gerners (soup):
    try:
        gerners = []
        # Find the div with the specific class and extract the style attribute
        var = soup.find('div', class_='series-gernes')

        if var:
            gerner = var.findAll("a")

            for gerner in gerner:
                genre_text = gerner.get_text().replace('\r', '').replace('\n', '').replace('\t', '').strip()
                # print(f"Extracted genre: {genre_text}")  # In thử từng thể loại
                if genre_text:
                    gerners.append(genre_text)
                    # gerners.append(gerner.contents[0])

            return gerners
        else:
            print("no gerner found")
            return None  
    except Exception as err:
        print("Lỗi ở đâu đó:" , err)
        return None


# # Send a GET request to fetch the content of the page
# response = requests.get("https://docln.net/truyen/139-that-nghiep-tai-sinh")

# # Parse the content with BeautifulSoup
# soup = BeautifulSoup(response.content, 'html.parser')

# test = extract_gerners(soup)
# print(test)
