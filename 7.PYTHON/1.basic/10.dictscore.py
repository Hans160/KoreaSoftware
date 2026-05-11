import random

# 무작위 이름 후보 리스트
name_list = [
    "김민준", "이서준", "박도윤", "최하준", "정지후", 
    "강지유", "조하윤", "윤서아", "장다은", "임나은",
    "한준서", "오민서", "서주원", "송예준", "권지안",
    "황지호", "안소율", "남현우", "신유나", "유도현"
]

# 중복 없이 10명의 이름을 선택하여 랜덤 점수 부여
# { "이름": 점수 } 형식의 딕셔너리 생성
students = {name: random.randint(0, 100) for name in random.sample(name_list, 10)}

# 결과 출력
print("students = {")
for name, score in students.items():
    print(f"    \"{name}\": {score},")
print("}")

def get_a_student(students):
    a_students = []
    for name, score in students.items():    #dict의 요소를 하나씩 가져옴
           if score >= 90:
            a_students.append(name)
    return a_students

print(get_a_student(students))