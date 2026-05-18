# pip install python-dotenv
import csv
import os
import requests
from dotenv import load_dotenv


load_dotenv() # .env 파일을 읽어서 해당 key/value를 메모리(환경변수)에 올려둠

API_KEY = os.getenv('YOUTUBE_API_KEY')


main_video_url = 'https://www.googleapis.com/youtube/v3/videos'

video_ids = []

with open("search_results.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        video_ids.append(row['video_id'])

# print(video_ids)


params = {
    'part': 'snippet,statistics',
    'id': ','.join(video_ids),
    'key': API_KEY
}

response = requests.get(main_video_url, params=params)
data = response.json()

# 최종결과물
table =[]

# 테이블 헤더
table_headers = ['index', 'title', 'view count', 'like count', 'comment count', 'video url']

with open("video_stats.csv", "w", encoding="utf-8", newline='') as file:
    writer = csv.writer(file)
    writer.writerow(table_headers)
    
    for item in data['items']:
        video_id = item['id']
        title = item['snippet']['title']
        stats = item['statistics']
        view_count = stats.get('viewCount', '0') # viewCount가 없는 경우 0으로 처리
        like_count = stats.get('likeCount', '0') # likeCount가 없는 경우 0으로 처리
        comment_count = stats.get('commentCount', '0') # commentCount가 없는 경우 0으로 처리


        writer.writerow([video_id, title, view_count, like_count, comment_count])
