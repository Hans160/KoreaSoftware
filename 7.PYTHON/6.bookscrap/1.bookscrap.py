# 1. books.toscrape.com 에 접속해서 페이지를 받아본다
# 2. DOM 을 bs4로 구성한다.
# 3. 첫 페이지의 도서명,평점,가격을 받아온다
# 4. csv파일로 저장한다.

import requests
from bs4 import BeautifulSoup
import csv

url = "https://books.toscrape.com/"
resp = requests.get(url)

# print(resp)

soup = BeautifulSoup(resp.text, "html.parser")

# print(soup)

title = soup.find("title")
print(title)
# #default > div > div > div > div > section > div:nth-child(2) > ol > li:nth-child(1) > article > h3 > a

first_book = soup.select_one("article.product_pod h3 a")

# print(first_book)

if first_book:
    # 'title' 속성에서 잘리지 않은 전체 도서명을 가져옵니다.
    first_title = first_book.get("title")
    print(first_title)


# #default > div > div > div > div > section > div:nth-child(2) > ol > li:nth-child(1) > article > p


star_rating_element = soup.select_one("p.star-rating")

# # 2. class 속성 가져오기 
# # ['star-rating', 'Three'] 형태의 리스트가 반환됩니다.
classes = star_rating_element['class']

# # 3. 두 번째 인덱스(Three) 출력
rating = classes[1]
print(rating)  # 출력: Three


# #default > div > div > div > div > section > div:nth-child(2) > ol > li:nth-child(1) > article > div.product_price > p.price_color

price_element = soup.select_one("p.price_color")

price = price_element.text.strip()
print(price)

data ={"도서명" : first_title, "평점" : rating, "가격" : price}


books = soup.select("article.product_pod")
# print(books)

rating_map ={
    "One" : 1,
    "Two" : 2,
    "Three" : 3,
    "Four" : 4,
    "Five" : 5
}

for book in books:
    title = title = book.select_one("h3 a").get("title")
    star_rating = book.select_one("p.star-rating").get("class")[1]
    rating_num = rating_map[star_rating]
    price = book.select_one("p.price_color").text.strip()
    price1 = price.replace("£", "")

    data ={"도서명" : title, "평점" : rating_num, "가격" : price1}

    with open("books.csv", "a", newline="", encoding="utf-8") as f:
        fieldnames = ["도서명", "평점", "가격"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerow(data)