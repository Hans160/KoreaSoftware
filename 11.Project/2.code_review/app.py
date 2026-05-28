import os
from dotenv import load_dotenv
# 웹 서비스 기본 프레임워크
from flask import Flask, send_from_directory, request, jsonify
from openai import OpenAI

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

app = Flask(__name__, static_folder='public')

@app.route('/')
def index():
    return send_from_directory('public', 'index.html')

@app.route('/api/codecheck', methods=['POST'])
def code_check():
    # 1. 프런트엔드에서 보낸 JSON 데이터 받아오기
    data = request.get_json()
    if not data or 'code' not in data:
        return jsonify({'result': '오류: 소스코드가 전송되지 않았습니다.'}), 400
    
    user_code = data['code'] # 프런트엔드에서 전송된 실제 소스코드

    # [수정] 문자열 앞에 f를 붙여 {user_code} 값이 정상적으로 주입되도록 수정
    prompt = (f"다음 코드의 보안 취약점을 분석해줘:\n"
              f"각 취약점에 대해 해당 코드의 라인번호, 코드 스니펫, 취약점 설명과 개선 방안을 간단하게 설명해줘. 코드 내의 주석은 무시해줘\n\n"
              f"소스코드:\n{user_code}\n\n"
              )
    
    try:
        # 2. ChatGPT API 요청하기
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system", 
                    "content": "당신은 소스코드 전문가입니다. 제출된 소스코드의 취약점을 분석하고 개선된 코드를 제시하세요."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ]
        )
        
        # 3. [수정] OpenAI 최신 표준 객체 접근 문법으로 안전하게 변경
        analysis_result = response.choices[0].message.content
        return jsonify({'result': analysis_result})

    except Exception as e:
        return jsonify({'result': f'API 호출 중 오류 발생: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
