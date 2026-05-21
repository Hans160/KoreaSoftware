import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)
DATABASE = 'board.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = get_db()
    # Retrieve posts descending by id to show newest first
    posts = conn.execute('SELECT id, title, message, created_at FROM posts ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

@app.route('/add', methods=['POST'])
def add_post():
    title = request.form.get('title', '').strip()
    message = request.form.get('message', '').strip()
    
    if not title or not message:
        conn = get_db()
        posts = conn.execute('SELECT id, title, message, created_at FROM posts ORDER BY id DESC').fetchall()
        conn.close()
        return render_template('index.html', posts=posts, error="제목과 내용을 모두 입력해 주세요.")
    
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    conn = get_db()
    conn.execute('INSERT INTO posts (title, message, created_at) VALUES (?, ?, ?)', (title, message, now_str))
    conn.commit()
    conn.close()
    
    return redirect(url_for('index'))

@app.route('/delete/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    conn = get_db()
    conn.execute('DELETE FROM posts WHERE id = ?', (post_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
