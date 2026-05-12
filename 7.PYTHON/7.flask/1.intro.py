from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <html>
        <head>
            <title>웰컴투 마이 홈</title>
            <style>
            p {
             color: red;
            }
         </head>
        <body>
            <h1>웰컴투 마이 홈</h1>
            <p>본문1</p>
            <p>본문2</p>
            <p>본문3</p>
            <p>본문4123</p>
        </body>
    </html>
    """

if __name__ == '__main__':
    app.run(debug=True, port=5000)  # 이거 나중에 개발 끝나고 배포/운영하는 곳에서는 꼭 제거해야한다
