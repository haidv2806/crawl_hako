import requests
from bs4 import BeautifulSoup


def extract_description (soup):
    try:
        # Find the div with the specific class and extract the style attribute
        var = soup.find('div', class_='summary-content')

        if var:
            # Lấy toàn bộ nội dung HTML bên trong div (bao gồm các thẻ <p>)
            description = var.decode_contents().strip()
            return description
        else:
            print("no description found")
            return None  
    except Exception as err:
        print("Lỗi ở đâu đó" , err)
        return None

# # Send a GET request to fetch the content of the page
# response = requests.get("https://docln.net/truyen/259-toi-la-nhen-thi-sao")

# # Parse the content with BeautifulSoup
# soup = BeautifulSoup(response.content, 'html.parser')

# test = extract_description(soup)
# print(test)
