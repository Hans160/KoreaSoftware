from bs4 import BeautifulSoup

html = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hello</title>
</head>
<body>
    <h1>Title</h1>
    <p>여기는 첫번째 파라그래프</p>
    <p>여기는 두번째 파라그래프</p>
    <p>안녕하세요</p>
    <p>안녕하세요</p>    
</body>
</html>
"""

soup = BeautifulSoup(html, 'html.parser')
print(soup)


heading = soup.find_all('h1')
paragraph = soup.find_all('p')

print(heading)
print(paragraph)