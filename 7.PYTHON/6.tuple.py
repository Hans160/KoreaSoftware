my_list = [1, 2, 3, 4, 5]
my_tuple = (1, 2, 3, 4, 5)

print(my_list)
print(my_tuple)

print(my_list[2])
print(my_tuple[2])

my_list[2] = 99
print(my_list)
# my_tuuple[2] = 99  # 튜플의 값을 쓸 수 없음

print(my_list[-1]) 
print(my_tuple[-1]) 

print(my_list[1:3])
print(my_tuple[1:3])

print(my_list[0:1])
print(my_tuple[0:1])

# 튜플을 받아 왔는데 쓰고싶다면?
my_newlist = list(my_tuple)
print(my_newlist)
my_newlist[2] = 88
print(my_newlist)

a,b,c =(1,2,3)
print(a,b,c)

a_person = ("John", 23, "Student")
print(a_person )
name, age, occ = a_person
print(name, age, occ)