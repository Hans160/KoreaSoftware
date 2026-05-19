from flask import Flask, render_template, request, redirect, url_for
from flask import session
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'secret_key'
app.config['permanent_session_lifetime'] = timedelta(minutes=5)

app.route('/')
def home():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)