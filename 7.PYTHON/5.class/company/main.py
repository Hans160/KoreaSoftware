from employee import Employee
from person import Person   

employee1 = Employee("James", 25, "Samsung")
employee2 = Employee("Tom", 30, "LG")
employee3 = Person("John", 35)

employee1.greet()
employee2.greet()
employee3.greet()

employee3.set_age(40)
print(employee3.get_name())