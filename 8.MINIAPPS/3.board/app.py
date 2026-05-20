from flask import Flask, send_from_directory, jsonify, request
from database import MyDatabase

app = Flask(__name__)
db = MyDatabase()

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

# 1. 게시글 생성
@app.route('/create', methods=['POST'])
def create():
    data = request.get_json() # 프론트엔드가 보낸 JSON 데이터를 가져옵니다.
    title = data.get('title')
    message = data.get('message')

    if not title or not message:
        return jsonify({'result': 'fail', 'message': '제목과 내용을 모두 입력해주세요.'}), 400

    sql = "INSERT INTO board (title, message) VALUES (?, ?)"
    db.execute(sql, (title, message))
    db.commit()
    
    return jsonify({'result': 'success', 'message': '글이 등록되었습니다.'})

@app.route('/list')
def list():
    sql = 'SELECT * FROM board'
    result = db.execute_fetch(sql)
    dict_list = [{'id': r['id'], 'title': r['title'], 'message': r['message']} for r in result]

    return jsonify(dict_list)

@app.route('/delete', methods=['POST'])
def delete():
    return jsonify({'result': 'success'})

@app.route('/modify', methods=['POST'])
def modify():
    return jsonify({'result': 'success'})


if __name__ == '__main__':
    app.run(debug=True, port=5001)
