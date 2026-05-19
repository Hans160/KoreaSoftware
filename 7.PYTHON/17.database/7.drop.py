import sqlite3

conn = sqlite3.connect('example.db')
cur = conn.cursor()

# 테이블 생성
cur.execute('''
    DROP TABLE users
''')

conn.commit()
conn.close()