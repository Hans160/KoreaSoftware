#pip install flask-session
from flask import Flask, session
from flask_session import Session   # 서버측에 세션을 저장하기 위한 확장 클라스

app = Flask(__name__)
app.secret_key = "abasdfasdfasdf" # 나만 아는 나의 세션 암호화 키. 이것도 .env 다루는거임
app.config['SESSION_TYPE'] = 'filesystem' # 세션 저장 방식 설정. 서버측에 파일로 저장하겠다.
app.config['SESSION_FILE_DIR'] = './sessions' # 세션 파일이 저장될 디렉토리 설정
app.config['SESSION_PERMANENT'] = False # 세션이 영구적이지 않도록 설정. 브라우저를 닫으면 세션이 사라진다.
app.config['SESSION_USE_SIGNER'] = True # 세션 데이터를 암호화하여 저장. 세션 쿠키에 서명 사용

Session(app) # 세션 확장 클라스를 초기화

@app.route("/set-session")
def set_session():
    session['username'] = 'spc2026' # 세션에 데이터를 저장
    session['fullname'] = '홍길동'
    session['dob'] = '1990-01-01'
    session['hobbies'] = ['coding', 'gaming', 'traveling']
    return "세션 저장 완료!!"

@app.route("/get-session")
def get_session():
    if 'username' in session:
        return f"세션에서 당신의 정보를 찾았습니다 {session['username'], session['fullname'], session['dob'], session['hobbies']}!"
    return "세션에 당신의 정보가 없습니다."

if __name__ == "__main__":
    app.run(debug=True)