from dbm import error

from flask import Flask, redirect, session, render_template,request, url_for

# Session 은 더이상 안함

app = Flask(__name__)
app.secret_key = 'my-ranmdom-secret-key'

users = [
    {"name": 'Alice', 'id': 'alice', 'pw': 'alice'},
    {"name": 'Bob', 'id': 'bob', 'pw': 'bob'},
    {"name": 'Charlie', 'id': 'charlie', 'pw': 'char'}

]

@app.route('/dashboard')
def welcome():
    user = session.get('user')
    return render_template('dashboard.html', user=user)

    
@app.route("/", methods=[ 'GET'])
def home():
    if session.get('user'):
        return redirect(url_for('welcome'))
    
    # 로그인 한적이 없을때, 그냥 첫 방문
    return render_template('index.html') # index.html 파일을 렌더링하여 반환
@app.route("/", methods=[ 'POST'])
def login():
    # 1. 요청에서 
    if request.method == 'POST':
        id = request.form.get('id')
        pw = request.form.get('pw')

    # 2. user db에서 이 사용자 매칭한다.
    user = None
    user =next((u for u in users if u['id'] == id and u['pw'] == pw), None)
   
    # 3. 사용자가 있으면?
    if user:    
        session['user'] = user['name'] # 세션에 사용자 이름 저장
        error = None
    else:
        error = "아이디 또는 비밀번호가 잘못되었습니다."
        return render_template('index.html', error=error)   

# 1. 사용자가 비밀번호 바꾸는 기능르 추가한다
# 1-1 method를 post로 확장
# 1-2 나의 users 안에서 나의 비번을 바꾼다
# 1-3 성공적으로 변경되면 나의 profile에서 확인한다.
# 1-4 '비밀번호 변경'을 눌렀을때 성공적으로 변경되었음을 알려준다.
@app.route("/profile")
def profile():
    user = session.get('user')
    if not user:
        return redirect(url_for('home'))
    return render_template('profile.html', user=user)

@app.route("/logout")
def logout():
    session.pop('user', None) # 세션에서 사용자 정보 제거
    return redirect(url_for('home')) # 홈으로 리다이렉트

if __name__ == "__main__":
    app.run(debug=True)


