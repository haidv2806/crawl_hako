import requests  
  
url = "http://localhost:8191/v1"  
headers = {"Content-Type": "application/json"}  
data = {  
    "cmd": "request.get",  
    "url": "https://docln.sbs/truyen/259-toi-la-nhen-thi-sao",  
    "maxTimeout": 60000  
}  
response = requests.post(url, headers=headers, json=data)  
print(response.text)