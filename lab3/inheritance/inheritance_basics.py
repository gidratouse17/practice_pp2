#1
# Inheritance allows us to define a class that inherits all the methods and properties from another class.

class Person:
  def __init__(self, fname, lname):
    self.firstname = fname
    self.lastname = lname

  def printname(self):
    print(self.firstname, self.lastname)
x = Person("John", "Doe")
x.printname()
x = Person("Mike", "Olsen")
x.printname()


class Person:
    def __init__(self, name):
        self.name = name
    def printname(self):
        print(self.name)
class Student(Person):
    pass
s = Student("Anna")
s.printname()


