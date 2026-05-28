from flask import Flask, send_from_directory, request, jsonify

app = Flask(__name__, static_folder='public')

reviews = []   # 사용자들의 댓글을 저장할 변수

@app.route('/')
def index():
    return send_from_directory('public', 'index.html')


# API 라우팅
@app.route('/api/reviews')                  # post 로 받기
def add_review():
    # reviews에 저장하기
    return jsonify({'message': '미완성'})

@app.route('/api/reviews')   # get 로 받기
def get_review():
    # revies 를 가져와서 반환하기
    return jsonify({'message': '미완성'})           

@app.route('/api/ai-summary') # get 로 받기
def get_ai_summary():
    # reviews를 가져와서
    return jsonify({'message': '미완성'})

if __name__ == '__main__':
    app.run(debug=True)