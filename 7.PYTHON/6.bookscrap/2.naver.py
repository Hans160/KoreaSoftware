import requests
from bs4 import BeautifulSoup
import csv

url = "https://www.naver.com/"
resp = requests.get(url)

soup = BeautifulSoup(resp.text, "html.parser")

