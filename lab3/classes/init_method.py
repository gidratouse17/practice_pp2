#1
class  Animal:
    def __init__(self, name):
        self.name = name

p1 = Animal("Poti")
print(p1.name)

#2
class Book:
    def __init__(self, title, pages):
        self.title = title
        self.pages = pages

b1 = Book("Demidovich", 500)
print(b1.title, b1.pages)

#3
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.area = width * height

r1 = Rectangle(8, 6)
print(r1.area)

#4
class Laptop:
    def __init__(self, model, ram):
        self.model = model
        self.ram = ram

l1 = Laptop("MacBook", 14)
print(l1.model, l1.ram)