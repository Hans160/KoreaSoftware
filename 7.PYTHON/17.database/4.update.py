import sqlite3

conn = sqlite3.connect('example.db')
cursor = conn.cursor()

cursor.execute('''
    UPDATE users SET age=? WHERE name=?
''', (33, 'bob'))
             
conn.commit()
conn.close()