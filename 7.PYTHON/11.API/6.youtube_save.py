# pip install python-dotenv
import csv
import os
import requests
from dotenv import load_dotenv


load_dotenv() # .env 파일을 읽어서 해당 key/value를 메모리(환경변수)에 올려둠

API_KEY = os.getenv('YOUTUBE_API_KEY')

url = 'https://www.googleapis.com/youtube/v3/search'

search_query = '파이썬 튜토리얼' \

params = {
    'part': 'snippet',
    'q': search_query,
    'type': 'video',
    'maxResults': 50,
    'key': API_KEY
}

response = requests.get(url, params=params)
data = response.json()
print(data)

with open('search_results.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['title', 'video_id', 'video_url', 'description'])  # 헤더 작성

    # csv 파일에 데이터 저장하기    
    for item in data['items']:
        title = item['snippet']['title']
        video_id = item['id']['videoId']
        video_url = f'https://www.youtube.com/watch?v={video_id}'
        description = item['snippet']['description']

        writer.writerow([title, video_id, video_url, description])  # 데이터 행 작성
        
        print(f'제목: {title}, URL: {video_url}, 설명: {description}')
        print('--'*20)