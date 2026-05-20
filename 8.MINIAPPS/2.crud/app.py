from flask import Flask, render_template, request, redirect, url_for
from flask import session, flash

from datetime import timedelta
import sqlite3

app = Flask(__name__)
app.secret_key = '1234' # 실무적으로는 이런 민감한 credential을 커밋하지않음.

app.permanent_session_lifetime = timedelta(minutes=5)
database = 'users.sqlite3' # 나의 파일명

def get_db_connection():
    conn = sqlite3.connect('database')
    conn.row_factory = sqlite3.Row     #  나의 결과를 다 Dict 포멧으로 관리
    return conn

def init_db():
    with app.app_context():            # flask app 초기화 완료된 후
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL, 
                password TEXT NOT NULL,
                email TEXT
            )
        ''')

        # 기본 계정 추가
        cur.execute("SELECT COUNT(*) AS count FROM users")
        count = cur.fetchone()['count']
        if count == 0:
            cur.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", ('user1', 'password1', 'user@example.com'))
            cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('user2', 'password2'))

        # 부팅시 계정 정보 출력
        cur.execute("SELECT * FROM users")
        rows = cur.fetchall()

        print('-' * 30)
        for row in rows:
            print(row['id'], row['username'], row['password'], row['email'])    #이건 다 Row를 Dict로 했기 때문에 이름으로 접근 가능
        print('-' * 30)

        conn.commit()
        conn.close()    

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/delete_account', methods=['GET', 'POST']) # 또는 POST만 허용
def delete_account():
    if 'user' not in session:
        return redirect(url_for('login'))
        
    username = session['user']
    
    # DB에서 유저 삭제
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE username = ?", (username,))
    conn.commit()
    conn.close()
    
    # 세션 비우기 (로그아웃) 및 홈으로 이동
    session.pop('user', None)
    flash("회원 탈퇴가 완료되었습니다. 그동안 이용해 주셔서 감사합니다.")
    return redirect(url_for('home'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    # 1. DB에서 나의 정보를 조회한다. 
    # 2. 그래서 아래에 넘겨준다.
    # 3. 해당 정보에 수정기능을 넣는다.
    # 보안: 로그인하지 않은 사용자는 로그인 페이지로 리다이렉트
    if 'user' not in session:
        flash("로그인이 필요한 서비스입니다.")
        return redirect(url_for('login'))
        
    username = session['user']

    # [3번 기능] POST 요청: 회원 정보 수정 처리
    if request.method == 'POST':
        new_password = request.form.get('password')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not new_password:
            flash("새 비밀번호를 입력해주세요.")
            return redirect(url_for('profile'))

        conn = get_db_connection()
        cur = conn.cursor()
        # 로그인한 사용자의 비밀번호 변경 SQL
        if password:
            cur.execute("UPDATE users SET password = ? WHERE username = ?", (new_password, username))
        if email:
            cur.execute("UPDATE users SET email = ? WHERE username = ?", (email, username))
        
        conn.commit()
        conn.close()

        flash("프로필 정보가 성공적으로 수정되었습니다.")
        return redirect(url_for('profile'))

    # [1번 & 2번 기능] GET 요청: DB에서 나의 정보를 조회하여 템플릿으로 전달
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = ?", (username,))
    user_data = cur.fetchone()
    conn.close()

    # 템플릿으로 유저 정보 넘겨주기
    return render_template('profile.html', user=user_data)
    

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')

        conn = get_db_connection()
        cur = conn.cursor()

        #추가 하기전, 해당 id를 가진 사용자가 있는지 확인
        cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        existng_user = cur.fetchone()

        if existng_user:
            flash("해당 ID는 사용할 수 없습니다.")
            conn.close()
            return redirect(url_for('signin'))
        
        cur.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", (username, password, email))
        conn.commit()
        conn.close()

        flash("회원가입 성공!")
        return redirect(url_for('login'))
    
    return render_template('signin.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user_data = cur.fetchone()
        conn.close()

        if user_data:
            session['user'] = username
            flash("로그인 성공!")
            return redirect(url_for('home'))
        else:       
            flash("로그인에 실패하였습니다")
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    flash("성공적으로 로그아웃이 되었습니다.")
    session.pop('user', None)
    return redirect(url_for('home'))


if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5001)       # 실무적으로는 꼭 끌것.