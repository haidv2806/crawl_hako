import requests
from bs4 import BeautifulSoup

def extract_image (soup):
    try:
        # Find the div with the specific class and extract the style attribute
        image = soup.find('div', class_='content img-in-ratio')

        if image and 'style' in image.attrs:
            style = image['style']
            
            # Extract the URL from the style string
            start = style.find("url('") + len("url('")
            end = style.find("')", start)
            image_url = style[start:end]
            
            return image_url
        else:
            print("Div not found or style attribute is missing.")
            return None
    except Exception as err:
        print("Lỗi ở đâu đó" , err)
        return None




# # Send a GET request to fetch the content of the page
# response = requests.get("https://docln.net/truyen/259-toi-la-nhen-thi-sao")

# # Parse the content with BeautifulSoup
# soup = BeautifulSoup(response.content, 'html.parser')


# test = extract_image(soup)
# print(test)