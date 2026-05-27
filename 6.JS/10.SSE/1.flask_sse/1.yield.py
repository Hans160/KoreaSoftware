# 우리가 하고 싶은것 : 서버에서 바뀌는 데이터를 알아서 반환한다.
# 아래처럼 함수를 부르ㅕㄴ 1을 줬다가.. 2가 됐으면 2를 주고.. 3이면 3을 주고..

def test():
    yield 1
    yield 2
    yield 3

x = test()
print(next(x))
print(next(x))
print(next(x))