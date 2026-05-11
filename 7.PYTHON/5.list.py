my_list = [1, 2, 3, 4, 5]

print(my_list)
print(len(my_list))

print(my_list[0])
print(my_list[4])

print(my_list[-1]) # 리스트의 거꾸로...(뒤로, 마지막)
print(my_list[-2]) # 뒤에서 2번째

print(my_list[1:3]) # 슬라이싱 [1] 포함하고 [3] 포함하지 않음
print(my_list[3:5])  
print(my_list[:2]) # 슬라이싱 [0] 포함하고 [2] 포함하지 않음

# 특정 위치에 맴버 추가하기
my_list.append(6)
print(my_list)

# 특정 위치에 맴버 추가하기
my_list.insert(2, 99)
print(my_list)

# 맴버 제거하기
my_list.remove(99)
print(my_list)

# 특정 인덱스의 요소 삭제하기
my_list.pop(3)
print(my_list)

my_list.clear()  # 리스트 통째로 비우기
print(my_list)

my_list = [5, 2, 1, 3, 4, 7, 6, 8 , 9]
print(my_list)

my_list.sort()   # 정렬을 하는데, 원본값을 변경하는 함수  sorted는 원본을 유지하고 복재본을 만듦
print(my_list)

my_list.reverse()
print(my_list)

copyed_list = my_list.copy() # 원본 리스트의  복재본을 만듦
print(copyed_list)

#리스트 컴프리헨션 ( 어려운대, 쓰면 매우매우 편함)
print('-'*30)
numbers = [x for x in range(10)]
print(numbers)
numbers = [x for x in range(5)]
print(numbers)
numbers = [x**2 for x in range(5)]
print(numbers)
numbers = [x for x in range(1,10) if x % 2 == 0]
print(numbers)
numbers = [x for x in range(1,10) if x % 2 == 1]
print(numbers)

list1 = [1,2,3]
list2 = [4,5,6]

list3 = list1 + list2
print(list3)

print(list1 * 3)