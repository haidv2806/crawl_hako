import requests
from bs4 import BeautifulSoup


def extract_status (soup):
    try:
        # Find the div with the specific class and extract the style attribute
        var = soup.findAll('span', class_='info-value')[2]

        if var:
            status = var.find("a").contents[0]

            return status
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

# test = extract_status(soup)
# print(test)