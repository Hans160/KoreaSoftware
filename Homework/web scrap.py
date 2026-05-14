from playwright.sync_api import sync_playwright
import time
import csv

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://makemyproject.net/shop/")
    page.wait_for_selector("div#products.grid")

    page.wait_for_selector("#uid")

    # 2. 아이디 입력 (#uid 속성 활용)
    page.locator("#uid").fill("user123")

    # 3. 비밀번호 입력 (#upw 속성 활용)
    page.locator("#upw").fill("password1234")

    # 4. 로그인 버튼 클릭 (#loginBtn 속성 활용)
    page.locator("#loginBtn").click()

    # 5. 로그인 완료 후 상품 목록이 로드될 때까지 2초 대기
    time.sleep(2)
    page.wait_for_selector("div#products.grid")
#products > div:nth-child(1) > div.row > a  제목
#products > div:nth-child(1) > div.muted 설명
#products > div:nth-child(1) > div.price > div.muted > span:nth-child(1) 정가
#products > div:nth-child(1) > div.price > div.muted > span:nth-child(2) 할인율
#products > div:nth-child(1) > div.price > div:nth-child(2) > strong 할인가
#div#sales.muted.sales-right 누적 판매량
#  페이지 데이터 수집

    page_num = 1
    results = []
    

    while True:
        print(f"\n--- {page_num}페이지 수집 시작 ---")

        # 1. 제목 길이
        titles_count = page.locator("#products > div.card").count()
        print(f"발견된 상품 개수: {titles_count}개")

        # 만약 페이지에 상품이 0개라면 수집 종료 (탈출 조건 1)
        if titles_count == 0:
            print("더 이상 수집할 상품 데이터가 없습니다. 수집을 종료합니다.")
            break

    
        for i in range(titles_count):
            title = page.locator(f"#products > div:nth-child({i+1}) > div.row > a").inner_text() #제목
            content = page.locator(f"#products > div:nth-child({i+1}) > div.muted").inner_text() #설명
            price = page.locator(f"#products > div:nth-child({i+1}) > div.price > div.muted > span:nth-child(1)").inner_text() #정가
            price_sale = page.locator(f"#products > div:nth-child({i+1}) > div.price > div:nth-child(2) > strong").inner_text() #할인가격
            print(title)
            

            #products > div:nth-child(1) > div.row > a  각 제목 클릭위치
            title_button = page.locator(f"#products > div:nth-child({i+1}) > div.row > a")
            title_button.click()  
            time.sleep(1.5)

            # ================== 클릭 후 본문 ==============================

            
            total_sale = page.locator(f"#sales").inner_text() # 누적 판매량
            print(total_sale)
            results.append({"누적 판매량": total_sale})

            reviews_count = page.locator("div.review").count() # 댓글 갯수
            print(f"발견된 댓글 개수: {reviews_count}개")
            
            reviews = []
            for j in range(reviews_count):
                review = page.locator(f"div.review:nth-child({j+1})").inner_text() 
                reviews.append(review.strip())
                
                
            reviews_str = "\n".join(reviews)

            results.append({
                "페이지": page_num,
                "제목": title.strip(),
                "설명": content.strip(),
                "정가": price.strip(),
                "할인가": price_sale.strip(),
                "누적 판매량": total_sale.strip(),
                "댓글": reviews_str
            })

            back_button = page.locator("body > p > a")
            back_button.click()

            time.sleep(1.5)


            # 1페이지가 아닐 때(2페이지 이상일 때) 뒤로가기를 하면 1페이지로 리셋되므로,
            # 현재 수집 중이던 원래 페이지 번호 버튼을 다시 강제로 클릭해서 화면을 복구합니다.
            if page_num > 1:
                current_page_button = page.locator(f"#pager > button:has-text('{page_num}')")
                if current_page_button.count() > 0:
                    current_page_button.click()
                    time.sleep(1.5) # 목록 데이터가 다시 로드될 때까지 대기
    
        # 다음 루프를 위해 가려고 하는 타겟 페이지 번호 계산
        target_page = page_num + 1 
        
        # nth-child 대신 버튼 내부의 글자(2, 3, 4...)를 직접 매칭하여 찾습니다.
        next_button = page.locator(f"#pager > button:has-text('{target_page}')")
    
        # 만약 다음 페이지 번호 버튼이 화면에 보이지 않는다면 종료 (탈출 조건 2)
        if next_button.count() == 0:
            print(f"다음 페이지 버튼({target_page}번)을 찾을 수 없습니다. 수집을 종료합니다.")
            break
        
        print(f"\n--- {target_page}페이지로 이동 중 ---")

        next_button.click()
        
        # 클릭 후 데이터가 비동기로 새로 완전히 로드될 때까지 대기
        time.sleep(2) 
        
        # 실제 변수 값을 증가시켜 다음 루프로 진입
        page_num += 1
        # --------------------------------------------------------

print("\n--- 💾 CSV 파일 저장 시작 ---")
csv_file_name = "scraped_products.csv"

# 인코딩을 'utf-8-sig'로 해야 엑셀(Excel)에서 열었을 때 한글이 깨지지 않습니다.
with open(csv_file_name, mode="w", encoding="utf-8-sig", newline="") as f:
    # CSV 파일 상단에 들어갈 컬럼 제목 정의
    fieldnames = ["페이지", "제목", "설명", "정가", "할인가", "누적 판매량", "댓글"]
    
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()  # 헤더 열 쓰기
    writer.writerows(results)  # 수집한 데이터 행 전체 쓰기

print(f"🎉 성공적으로 '{csv_file_name}' 파일로 저장되었습니다!")