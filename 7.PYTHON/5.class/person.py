class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        print(f"안녕하세요. 저는 {self.name}입니다.")

    def study(self, subject):
        print(f"{self.name}는 {subject}을 공부하는 중입니다.")

person1 = Person("Alice", 25)
person2 = Person("Bob", 30)

person1.greet()
person2.greet()