from flask import Flask, render_template, request
from flask import redirect, url_for
from flask import session
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'my-random-key'
app.config['permanent_session_lifetime'] = timedelta(minutes=5) # 세션의 유효기간을 1일로 설정 (초 단위)    

# Session 은 더이상 안함 -> 나중엔 이게 DB 에서 대체함

items = [
    {'id': 'item1', 'name': '햄버거', 'price': 3000},
    {'id': 'item2', 'name': '치킨', 'price': 2000},
    {'id': 'item3', 'name': '피자', 'price': 3000},
]

@app.route('/')
def index():
    return render_template('product.html', items=items)

@app.route('/add_to_cart/<item_id>')
def add_to_cart(item_id):
    # 세션에 'cart' 저장소가 없으면 빈 리스트([])로 새로 만들어 줍니다.
    print("장바구니에 담을 상품: ", item_id)
    if 'cart' not in session:
        session['cart'] = {}

    if item_id in session['cart']:
        session['cart'][item_id] += 1
    else:
        # 장바구니에 담을 상품이 실제로 존재하는가??
        session['cart'][item_id] = 1

    # session.modified = True # 세션이 변경되었음을 Flask에게 알려줍니다. (세션이 딕셔너리 형태로 저장되어 있기 때문에, 내부적으로 변경이 감지되지 않을 수 있습니다.)
    return redirect(url_for('index'))

@app.route('/cart')
def view_cart():
    cart_items = {}
    total_price = 0
    for item_id, quantity in session.get('cart', {}).items():
        item = next((i for i in items if i['id'] == item_id), None)
        cart_items[item_id] = {
            'name': item['name'],
            'quantity': quantity,
            'price': item['price'],
            
        }
        total_price += item['price'] * quantity
    
    return render_template('cart.html', cart_items=cart_items, total_price=total_price)


if __name__ == "__main__":
    app.run(debug=True)