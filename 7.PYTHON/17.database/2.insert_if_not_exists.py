import sqlite3

conn = sqlite3.connect('example.db')
cur = conn.cursor()

cur.execute('''
    SELECT COUNT(*) FROM users
''')

COUNT = cur.fetchone()[0]
print(COUNT)

if COUNT == 0:
    cur.execute('''
        INSERT INTO users (name, age) VALUES ('Alice', 30)
    ''')

    cur.execute('''
        INSERT INTO users (name, age) VALUES (?,?)
    ''', ('Bob', 25))
else:
    print('users table already exists')
    
conn.commit()
conn.close()