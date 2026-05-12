from person import Person

class Driver(Person):
    def __init__(self, name, age, car):
        super().__init__(name, age)
        self.car = car

    def driver(self):
        print(f"{self.name}는 {self.car} 운전을 시작합니다.")

    def drive_fast(self):
        print(f"{self.name}는 {self.car} 과속 운전을 시작합니다.")