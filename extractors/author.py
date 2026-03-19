import requests
from bs4 import BeautifulSoup


def extract_author (soup):
    try:
        # Find the div with the specific class and extract the style attribute
        var = soup.find('span', class_='info-value')

        if var:
            author = var.find("a").contents[0]
            return author
        else:
            print("no author found")
            return None  
    except Exception as err:
        print("Lỗi ở đâu đó" , err)
        return None


# # Send a GET request to fetch the content of the page
# response = requests.get("https://docln.net/truyen/259-toi-la-nhen-thi-sao")

# # Parse the content with BeautifulSoup
# soup = BeautifulSoup(response.content, 'html.parser')

# test = extract_author(soup)
# print(test)
