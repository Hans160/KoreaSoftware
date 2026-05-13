from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)

users = [
    {'name': 'Alice', 'age': 25, 'phone': '123-456-7890'},
    {'name': 'Bob', 'age': 30, 'phone': '123-555-7890'},
    {'name': 'Charlie', 'age': 27, 'phone': '321-777-7890'},
    {'name': 'David', 'age': 25, 'phone': '321-999-7890'}
]

@app.route('/search/')
def search():
    result = None

    name = request.args.get('name')
    age = request.args.get('age')
    phone = request.args.get('phone')

    if name:
        result = [u   for u in users   if name.lower() in u['name']]
    if age:
        result = [u   for u in users   if int(age) == u['age']]
    if phone:
        result = [u   for u in result   if u['phone'].startswith(phone)] 
    return jsonify(result)









    # 쿼리 파라미터로 name, age, phone 로 검색해서 결과를 반환

    # if query:
    #     for user in users:
    #         if query.lower() in user['name'].lower() or \
    #             str(query) in str(user['age']) or \
    #             query.lower() in user['phone'].lower():
    #             result.append(user)

    # else:
    #     return jsonify({"message": "user not found"})

    # return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port = 5000)