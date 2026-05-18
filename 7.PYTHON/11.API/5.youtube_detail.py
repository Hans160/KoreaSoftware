# pip install python-dotenv
import os
import requests
from dotenv import load_dotenv


load_dotenv() # .env 파일을 읽어서 해당 key/value를 메모리(환경변수)에 올려둠

API_KEY = os.getenv('YOUTUBE_API_KEY')

search_url = 'https://www.googleapis.com/youtube/v3/search'
main_video_url = 'https://www.googleapis.com/youtube/v3/videos'

search_query = '파이썬 튜토리얼' \

params = {
    'part': 'snippet',
    'q': search_query,
    'type': 'video',
    'maxResults': 50,
    'key': API_KEY
}

response = requests.get(search_url, params=params)
data = response.json()


search_results = []

for item in data['items']:
    title = item['snippet']['title']
    video_id = item['id']['videoId']
    video_url = f'https://www.youtube.com/watch?v={video_id}'
    description = item['snippet']['description']

    search_results.extend(data['items'])

    print(f'제목: {title}, URL: {video_url}, 설명: {description}')
    print('--'*40)

# 최종결과물
table =[]

#가져오고 싶은 추가 정보
table_headers = ['index', 'title', 'view count', 'video url']
for index, result in enumerate(search_results, start=1):
    title = result['snippet']['title']
    video_id = result['id']['videoId']
    video_url = f'https://www.youtube.com/watch?v={video_id}'

    # 공식 문서를 보고 어떤 파라미터를 넣어야 내가 원하는 통계(조회수) 가 나오는지 찾아보기
    video_params = {
        'part': 'statistics',
        'id': video_id,
        'key': API_KEY
    }

    video_response = requests.get(main_video_url, params=video_params)
    video_data = video_response.json()

    if 'items' in video_data and video_data['items']:
        view_count = video_data['items'][0]['statistics']['viewCount']
    else:
        view_count = '조회수 정보 없음'

    table.append({
        'index': index,
        'title': title,
        'view count': view_count,
        'video url': video_url
    })

print(table)    
