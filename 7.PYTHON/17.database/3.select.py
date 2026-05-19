import sqlite3

conn = sqlite3.connect('example.db')
cursor = conn.cursor()

cursor.execute('''
    select * from users                              
''')                

# 커서야.. 니가 실행한 결과 다 나 저ㅜ..
rows = cursor.fetchall()
print(rows)
conn.close()