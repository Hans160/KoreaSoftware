import requests

url = requests.get("http://www.example.com")

response = requests.get(url)

html = response.text

print(html)

print("-"*30)

# 원하는 태그 찾아오기
while "<h1>" in html:
    start = html.find("<h1>")
    end = html.find("</h1>")

    text = html[start:end+4]
    print(text)