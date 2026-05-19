import sqlite3

conn = sqlite3.connect('example.db')
cur = conn.cursor()

cur.execute('''
    INSERT INTO users (name, age) VALUES (?,?)
''', ('Alice', 30))

cur.execute('''
    INSERT INTO users (name, age) VALUES ('bob', 25)
''')

conn.commit()
conn.close()