# 툴들 추가
# 1. 네이버 뉴스를 가져온다. 배웠음 (API-key)
# 2. 구글 검색으로 기업 개요/최근 정보를 조회한다. 배웠음 (API-key)
# 3. 환율을 조회한다.
# 4. 주가를 조회한다.
import os
import requests
import re
import urllib.parse
from langchain_core.tools import tool
@tool
def get_news(query: str) -> str:
    """네이버 뉴스에서 키워드로 최신 기사 제목/링크를 검색한다."""
    #1. .env 환경 변수에서 발급받은 네이버 API-Key을 읽어서 메모리에 올려둠
    client_id = os.getenv("NAVER_CLIENT_ID")
    client_secret = os.getenv("NAVER_CLIENT_SECRET")
    
    if not client_id or not client_secret:
        return "오류: .env 파일에 NAVER_CLIENT_ID 또는 NAVER_CLIENT_SECRET 환경 변수가 설정되지 않았습니다."
        
    try:
        # 2. 검색어 URL 인코딩 처리 및 API 요청 변수 설정
        encoded_query = urllib.parse.quote(query)
        # display=5 (5개 노출), sort=sim (유사도순 정렬 / 최신순은 date)
        url = "https://openapi.naver.com/v1/search/news.json"
        
        # 3. 네이버 API 필수 헤더 셋팅
        headers = {
            "X-Naver-Client-Id": client_id,
            "X-Naver-Client-Secret": client_secret
        }
        
        # 4. HTTP GET 요청 실행
        response = requests.get(
            url,
            params={"query": encoded_query, "display": 5, "sort": "date"},
            headers=headers)
        
        if response.status_code != 200:
            print(f"\n[네이버 API 디버깅 로그] 에러 발생 코드: {response.status_code}")
            print(f"[네이버 API 디버깅 응답 내용]: {response.text}")
            return f"네이버 뉴스 API 요청 실패 (에러 코드: {response.status_code})"
            
        data = response.json()
        items = data.get("items", [])
        
        if not items:
            return f"'{query}'에 대한 네이버 뉴스 검색 결과가 없습니다."
            
        # 5. 결과 가공 (HTML 태그 제거 작업 포함)
        news_list = []
        for item in items:
            # 네이버 API 결과 특유의 <b> 태그나 &quot; 같은 특수문자 제거 정제
            title = item["title"].replace("<b>", "").replace("</b>", "").replace("&quot;", '"')
            description = item["description"].replace("<b>", "").replace("</b>", "").replace("&quot;", '"')
            link = item["link"]
            
            news_list.append(f"- 제목: {title}\n  요약: {description}\n  링크: {link}")
            
        return "\n\n".join(news_list)
        
    except Exception as e:
        return f"네이버 뉴스 API 호출 중 예외 발생: {str(e)}"
    
@tool
def get_company_info(company_name: str) -> str:
    """구글 검색(Serper)으로 기업 개요/최근 정보를 조회한다."""
    
    # 1. .env 파일로부터 구글 검색 API 연동 키 로드
    key = os.getenv("SERPER_API_KEY")
    
    if not key:
        return "오류: .env 파일에 SERPER_API_KEY 가 미설정 되어 기업 정보 검색이 불가합니다."
        
    return "미구현"
@tool
def get_exchange_rate(base: str = "USD", target: str = "KRW") -> str:
    """무료 환율 API를 통해 기준 통화 대비 주요 국가들의 실시간 환율을 조회합니다."""
    resp =requests.get("https://open.er-api.com/v6/latest/{base}}")
    

@tool
def get_stock_price(ticker):
    """yfinance를 활용하여 주식의 최신 영업일 주가 정보(종가, 고가, 저가)를 조회합니다. 한국 주식(예: 삼성전자, SK하이닉스)은 티커 대신 한글명을 입력해도 내부적으로 처리됩니다."""

    # pip install yfinance
    import yfinance as yf
    data = yf.Ticker(ticker).history(period="1d")
    if data.empty:
        return f"'"


TOOLS = [get_news, get_company_info, get_exchange_rate, get_stock_price]

