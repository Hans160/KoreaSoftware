# 문자열을 변수에 할당하면 string 타입이 됨
s = "Hello, World"

print(s)
print(s.lower())
print(s.upper())
print(s.capitalize()) # 각 문장의 시작은 대문자
print(s.title())      # 각 단어의 시작은 대문자

s = "     Hello,      World    "
print(s.strip()) # 앞뒤 불필요한 공백제거
print(s.strip() + "!!")  # 앞뒤 불필요한 공백제거
print(s.lstrip() + "!!") # 앞 불필요한 공백 제거
print(s.rstrip() + "!!") # 후 불필요한 공백 제거

print(s.split()) # 공백에 따라 분리

s = "apple banana cherry"
print(s.split()) # 공백에 따라 분리

s= "apple,banana,cherry"
print(s.split(',')) # 공백에 따라 분리

s_list=s.split(',')
print(s_list)
print(",".join(s_list))

s = "Hello, World"
print(s)
print(s.startswith("Hello"))   #True
print(s.startswith("hello"))   #False
print(s.endswith("World"))     #True


s = "김길동"
print(s.startswith("김"))   #True
print(s.startswith("홍"))   #False