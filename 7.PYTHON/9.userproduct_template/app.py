from flask import Flask, render_template, request

# 1. /user 라는 경로를 만들고 URL파라미터를 기반으로 사용자를 조회할수 있게 한다.
#    /user는 모든 사용자 /user/1 홍길동 /user/2 김철수 등
# 2. /product 로 쿼리 파라미터를 기반으로 상품을 조회할수 있다
#    /product는 모든 상품, /product?id=101 로 상품 검색 ?name 으로도 상품 검색

app = Flask(__name__)

# dict 에 dict 는 인덱싱을 통한 빠른 조회 가능 (굳이 for u in users 이런거 안해도 됨)
users = {
    1: {"id": 1, "name": "홍길동", "email": "hong@example.com"},
    2: {"id": 2, "name": "김철수", "email": "kim@example.com"},
    3: {"id": 3, "name": "이영희", "email": "lee@example.com"},
    4: {"id": 4, "name": "박민수", "email": "park@example.com"},
    5: {"id": 5, "name": "최지우", "email": "choi@example.com"},
}

products = {
    101: {"id": 101, "name": "Laptop", "price": 1200},
    102: {"id": 102, "name": "Keyboard", "price": 80},
    103: {"id": 103, "name": "Mouse", "price": 40},
    104: {"id": 104, "name": "Monitor", "price": 300},
    105: {"id": 105, "name": "Headset", "price": 150},
}

# 메인 홈 화면 (index.html 연동)
@app.route("/")
def home():
    return render_template("index.html")

# 1. 사용자 조회 라우트 (templates/user.html 연동)
@app.route('/user')
@app.route('/user/<int:user_id>')
def user(user_id=None):
    if user_id is None:
        # /user 요청 시 전체 사용자 딕셔너리 전달
        return render_template("user.html", users=users, user=None)
    
    # /user/<user_id> 요청 시 특정 사용자 데이터만 전달
    selected_user = users.get(user_id)
    return render_template("user.html", users=None, user=selected_user)

# 2. 상품 조회 라우트 (templates/product.html 연동)
@app.route('/product')
def product():
    product_id = request.args.get('id')
    product_name = request.args.get('name')

    # id 검색 (?id=101)
    if product_id:
        try:
            target_id = int(product_id)
            prod_data = products.get(target_id)
            # 검색 결과를 딕셔너리 형태로 감싸서 전달
            filtered_products = {target_id: prod_data} if prod_data else {}
            return render_template("product.html", products=filtered_products)
        except ValueError:
            return render_template("product.html", products={})

    # name 검색 (?name=Laptop)
    if product_name:
        filtered_products = {
            k: v for k, v in products.items() 
            if product_name.lower() in v['name'].lower()
        }
        return render_template("product.html", products=filtered_products)

    # 파라미터가 없으면 모든 상품 전달
    return render_template("product.html", products=products)

if __name__ == "__main__":
    app.run(debug=True)


