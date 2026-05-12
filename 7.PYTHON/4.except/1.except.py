try :
    result = 10 / 0
except ZeroDivisionError:
    print("0으로 나눌 수 없습니다.")
except Exception as e:
    print("알 수 없는 오류입니다")

print("다음 코드 정상진행")    

try :
    number = int("hello")
except ValueError:
    print("숫자로 변환할 수 없습니다.")
except Exception as e:
    print("알 수 없는 오류입니다")

print("다음 코드 정상진행")

alist = [1,2,3 ]
try :
    number = alist[3]
except IndexError:
    print("리스트에 원소가 없습니다.")
except Exception as e:
    print("알 수 없는 오류입니다")

print("다음 코드 정상진행")