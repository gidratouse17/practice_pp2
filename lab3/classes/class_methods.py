#1
class Ibiray:
    def __init__(self, name):
        self.name = name

    def speak(self):
        print(f"{self.name} says: Kel balalar, okylyk")

r1 = Ibiray("Altynsarin")
r1.speak()

#2
class Bank:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        print(f"New balance: {self.balance}")

acc = Bank("Karina", 20000)
acc.deposit(2222)

#3
class Student:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade

    def get_info(self):
        return f"{self.name} has grade {self.grade}"

s1 = Student("Akyltai", "A+")
print(s1.get_info())

#4
class my_friend:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f"{self.name} is {self.age} years old"

f1 = my_friend("Katya", 17)
print(f1)