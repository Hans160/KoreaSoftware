print('*')
print('**')
print('***')
print('****')
print('*****')

print('\n - 1 -')
for i in range(1,6): #1부터 출발해서 6을 포함하지 않는것
    print('*' * i)

print('\n - 2 -')   
n = 5 
for i in range(1,6): 
    print(" " *(5-i) + '*' * i)

print('\n - 3 -')   
n = 5 
for i in range(1,6): 
    print(" " *(5-i) + '*' * (2*i-1))