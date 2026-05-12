from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://news.naver.com/section/105")

    # 네이버 뉴스 본문 제목의 일반적인 선택자 (헤드라인 제목)
    #_SECTION_HEADLINE_LIST_647cv > li:nth-child(1) > div > div > div.sa_text > a > strong
    headlines = page.locator(".section_article.as_headline a.sa_text_title")
    print("헤드라인 갯수 :", headlines.count())

    for i in range(headlines.count()):
        news = headlines.nth(i)

        # 제목 가져오기
        title = news.inner_text().strip()

        # 링크 가젹오기
        href = news.get_attribute("href")

        print(f"{i+1}. {title}\n{href}")
    input("엔터를 누르면 종료될테야")