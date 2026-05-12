from flask import Flask, jsonify

app = Flask(__name__)

users = [
    {'name': 'Alice', 'age': 25, 'phone': '010-1234-5678'},
    {'name': 'Bob', 'age': 30, 'phone': '010-2345-6789'},
    {'name': 'Charlie', 'age': 35, 'phone': '010-3456-7890'}
]
# 파이썬의 리스트 폼, 각각의 리스트에는 딕셔너리

@app.route('/')
def main():
    return jsonify(users)  #우리의 백엔드 list/dict 구조를 웹이 좋아하는 json보여줌

@app.route('/user/<name>')
def get_user_by_name(name):
    print("사용자입력값: ", name)
    user = None
    for u in user:
        if u['name'] == name:
            user = u
            break   # break 끝

    if user:
        return jsonify(user)
    else:
        return "<h1>사용자 : {name}</h1>"  # html끝

if __name__ == '__main__':
    app.run(debug=True, port=5000)