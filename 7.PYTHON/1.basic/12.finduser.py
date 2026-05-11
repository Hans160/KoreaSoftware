users = [
    {"name": "김민준", "age": 32, "location": "서울", "car": "테슬라 모델3"},
    {"name": "이서준", "age": 28, "location": "부산", "car": "아이오닉6"},
    {"name": "박도윤", "age": 45, "location": "경기", "car": "제네시스 G80"},
    {"name": "최하준", "age": 35, "location": "인천", "car": "아반떼"},
    {"name": "정지후", "age": 41, "location": "대구", "car": "쏘렌토"},
    {"name": "강지유", "age": 29, "location": "대전", "car": "BMW 3시리즈"},
    {"name": "조하윤", "age": 38, "location": "광주", "car": "벤츠 C클래스"},
    {"name": "윤서아", "age": 24, "location": "울산", "car": "없음"},
    {"name": "장다은", "age": 31, "location": "세종", "car": "카니발"},
    {"name": "임나은", "age": 27, "location": "제주", "car": "캐스퍼"}
]

def find_user(name):
    for user in users:
        if user['name'].startswith(name):   # 앞글자 즉 성씨로 찾기
            print(user)

find_user("김")
find_user("강")

print('-' * 30)
print('-' * 30)

def find_user_and_return(name):
    found= []  # 찾은 사용자를 담을 바구니(리스트 변수)

    for user in users:
        if user['name'].startswith(name):   # 앞글자 즉 성씨로 찾기
            found.append(user)
            return found

found_users = find_user_and_return("강")
print("찾은 사용자: ", found_users)

def find_users2():
    """이름 또는 나이를 입력받아 매칭되는 사람을 반환한다"""
    name = input("이름: ")
    age = int(input("나이: "))

    for user in users:
        if user['name'] == name or user['age'] == age:
            return user
        
print(find_users2())

search_condition1 = {
    "name": "박도윤"
}

search_condition2 = {
    "name": "박도윤",
    "age": 45   
}

search_condition3 = {
    "age": 45
}

# def find_usrs2_best(condition) :
#     found = []
#     for user in users:
#         if user.get("name") == condition.get("name","") and user.get("age") == condition.get("age",0) and \
#             user.get("location") == condition.get("location",""):
#             found.append(user)
#     return found
