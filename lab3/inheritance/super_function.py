class First:
    def go(self): print("First go")
class Second(First):
    def go(self): super().go(); print("Second go")
Second().go()


class A:
    def show(self):
        print("Level A")
class B(A):
    def show(self):
        super().show()
        print("Level B")
B().show()


class Writer:
    def log(self):
        print("Writing")
class FileWriter(Writer):
    def log(self):
        super().log()
        print("File updated")
FileWriter().log()


class Device:
    def power(self):
        print("Device powered on")
class Phone(Device):
    def power(self):
        super().power()
        print("Phone is ready")
Phone().power()



class Person:
    def greet(self):
        print("Hello from Pupil")
class Student(Person):
    def greet(self):
        super().greet()
        print("Hello from Student")
Student().greet()
