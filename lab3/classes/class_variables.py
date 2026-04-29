#1
class Student:
    year = 1
    def __init__(self,name,uni):
        self.name = name
        self.university = uni
S1 = Student("Adilkhan","KBTU")
S2 = Student("Dariga", "ENU")

print(f"{S1.name} is studying at {S1.university} & he is {S1.year} year student")
print(f"{S2.name} is studying at {S2.university} & she is {S2.year} year student")

#2
class Course:
    duration = "6 months"   

    def __init__(self, title, teacher):
        self.title = title
        self.teacher = teacher

C1 = Course("History", "Valentina")
print(f"{C1.title} by {C1.teacher}")
print("Duration:", Course.duration)

#3
class Dorm:
    city = "Almaty"  

    def __init__(self, rooms, price):
        self.rooms = rooms
        self.price = price

A1 = Dorm(2 ,300000)
print(f"{A1.rooms} rooms - {A1.price}")
print("City:", Dorm.city)

#4
class Company:
    country = "Kazakhstan"   

    def __init__(self, name, position, salary):
        self.name = name      
        self.position = position
        self.salary = salary

E1 = Company("Sultan", "Director", 20000000)
print(f"{E1.name} {E1.position}: {E1.salary} salaryy")
print("Country:", Company.country)