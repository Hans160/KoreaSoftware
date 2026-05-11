# 딕셔너리
# 키:밸류로 쌍을 이루고 있는 자료구조
my_dict = {"name": "Alice", "age": 25, "location": "서울"}
print(my_dict)

# JSON 과 비슷하게 생겨서, 웹서비스 만들때 많이 사용함. 그렇다고 JSON은 아님
print(my_dict["name"])
print(my_dict["age"])
print(my_dict["location"])

my_dict["car"] = "BMW"
print(my_dict)

del my_dict["location"]
print(my_dict)

my_dict.pop("age")
print(my_dict)

my_dict.clear()
print(my_dict)

my_squares = {x: x**2 for x in range(10)}
print(my_squares)

print(my_squares.keys())
print(my_squares.values())
print(my_squares.items())