import requests

file = {'file': open('images/sample.jpg', 'rb')}
res = requests.post("http://localhost:8000/ocr", files=file)
print(res.json())
