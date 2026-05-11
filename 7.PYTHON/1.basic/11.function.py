def add_numbers(a, b):
    result = a+b
    return result

sum = add_numbers(3, 4)
print(f"두 수의 합은 {sum}이다.")

def add_numbers2(a, b):
   return a, b, a+b

input1, input2, sum = add_numbers2(3, 4)
print(f"인자1은 {input1}이고, 인자2은 {input2}이고, 합은 {sum}이다.")

def calculate_all(a, b):
    addition = a + b
    subtraction = a - b
    multiplication = a * b
    division = a / b
    return addition, subtraction, multiplication, division

add, sub, mul, div = calculate_all(3, 4)
print(f"덧셈은 {add}이고, 뻴셈은 {sub}이고, 곱셈은 {mul}이고, 나노셈은 {div}이다.")

add, _, mul, _ = calculate_all(5, 6)
print(f"덧셈은 {add}, 곱셈은 {mul}이다.")

print('-' * 30)

def create_profile(name, age, city="서울", job="학생"):
    profile = f"이름: {name}, 나이: {age}, 지역: {city}, 직업: {job}"
    return profile

print(create_profile("홍길동", 23))
print(create_profile("김길동", 25))
print(create_profile("박길동", 27))
print(create_profile("이길동", 27, "부산"))
print(create_profile("최길동", 27, "부산", "직장인"))

