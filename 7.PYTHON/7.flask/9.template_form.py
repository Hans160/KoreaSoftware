from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/login', methods=['POST'])  
def login():
    id = request.form.get['id']
    pw = request.form.get['pw']
    print(f"입력한 ID는 {id}, 비밀번호는 {pw}입니다.")

    return render_template('login.html', name=id)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['photo']
    print(file)
    return '파일 잘 받았음'
if __name__ == '__main__':
    app.run(debug=True, port=5000)