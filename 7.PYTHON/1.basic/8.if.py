print(' --- if 구문')

score = 80
if score >= 80:
    print('성적은 A+입니다.')
    grade = 'A+'
elif score >= 70:
    print('성적은 B입니다.')
    grade = 'B'
elif score >= 60:
    print('성적은 C입니다.')
    grade = 'C'
else:
    print('성적은 F입니다.')

print(f"이 학생의 점수는 {score}점이고, 학점은 {grade}입니다.")

month = 7
if month in [12,1,2]:
    season = "겨울"
elif month in [3,4,5]:
    season = "봄"
elif month in [6,7,8]:
    season = "여름"
elif month in [9,10,11]:
    season = "가을"
else:
    season = "알 수 없는"

print(f"{month}월은 {season}이다.")

height = 175 # cm
weight = 92 # kg
bmi = weight / (height/100)**2

if bmi < 18.5:
    category = "저체중"
elif bmi < 25:
    category = "정상"
elif bmi < 30:
    category = "과체중"
else:
    category = "비만"

print(f"이 사람의 BMI는 {bmi}인들로, {category}이다.")

username = 'admin'
password = '1234'

if username and password:   # username이 있는지, password이 있는지 파악
    if username == 'admin' and password == '1234':      
        print("관리자로 로그인 되었습니다")
    elif username == 'user' and password == '1234':
        print("일반 사용자로 로그인 되었습니다")
    else:
        print("잘못된 ID 또는 비밀번호입니다.")
else:
    print('유저네임과 비밀번호를 입력하세요.')