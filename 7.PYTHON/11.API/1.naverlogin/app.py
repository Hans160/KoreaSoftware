from flask import Flask, render_template, redirect, request, session, url_for
from dotenv import load_dotenv
import requests
import os

load_dotenv()

client_id = os.getenv("NAVER_CLIENT_ID")
client_secret = os.getenv("NAVER_CLIENT_SECRET")
callback_uri = os.getenv("NAVER_REDIRECT_URI")


app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

@app.route('/')
def index():
    user = session.get('user')
    return render_template('index.html', user=user)

@app.route('/api/naver/callback')
def naver_callback():
    code = request.args.get('code')
    state = request.args.get('state')  # 네이버가 콜백으로 다시 돌려준 state 값

    # 1. 접근 토큰(Access Token) 발급 요청 URL 수정
    # 네이버 로그인 시 보냈던 state 값과 동일한 값을 넘겨주어야 토큰이 발급됩니다.
    token_url = (
        f"https://naver.com?"
        f"grant_type=authorization_code&"
        f"client_id={client_id}&"
        f"client_secret={client_secret}&"
        f"code={code}&"
        f"state={state}"  # <--- 고정값 'Hello' 대신 네이버가 전달해준 state 변수를 그대로 사용합니다.
    )

    token_response = requests.get(token_url).json()
    print("=== [1단계] 네이버 토큰 발급 응답 ===")
    print(token_response)  # 토큰 요청 결과가 에러인지 정상인지 터미널에서 확인용

    access_token = token_response.get('access_token')

    # 토큰이 정상적으로 발급되지 않은 경우, 예외 처리로 차단
    if not access_token:
        error_msg = token_response.get('error_description', '토큰 발급 실패')
        return f"로그인 실패 (토큰 발급 오류): {error_msg}", 400

    # 2. 발급받은 토큰으로 프로필 정보 요청
    profile_url = "https://naver.com"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    profile_response = requests.get(profile_url, headers=headers)
    profile = profile_response.json()
    
    print("=== [2단계] 네이버 프로필 조회 응답 ===")
    print(profile)

    # 3. 세션 저장 및 마무리
    if "response" in profile:
        session["user"] = profile["response"]
        return redirect(url_for('index'))
    else:
        return f"사용자 정보 로드 실패: {profile.get('message', '알 수 없는 오류')}", 400



@app.route('/login')
def naver_login():

    AUTH_URL =(
        f"https://nid.naver.com/oauth2.0/authorize?"
        f"response_type=code&client_id={client_id}&"
        f"&redirect_uri={callback_uri}&state=Hello"
        
    )
    print(AUTH_URL)
    return redirect(AUTH_URL)
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True , port=5000)