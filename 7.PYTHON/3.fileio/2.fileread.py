with open("file.txt","r", encoding="utf-8") as file:
    content = file.read()
    print("파일 내용 :", content)


with open("file.txt","r", encoding="utf-8") as file:
    lines = file.readlines()
    for line in lines:
        print("파일 내용 :", line)