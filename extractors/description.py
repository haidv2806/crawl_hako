import requests
from bs4 import BeautifulSoup


def extract_description (soup):
    try:
        # Find the div with the specific class and extract the style attribute
        var = soup.find('div', class_='summary-content')

        if var:
            # Lấy nội dung text, loại bỏ các thẻ HTML (như <p>)
            description = var.get_text(separator='\n', strip=True)
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
