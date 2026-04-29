class Shape:
    def area(self):
        return 0
class Square(Shape):
    def __init__(self, a):
        self.a = a
    def area(self):
        return self.a * self.a
print(Square(5).area())


class TextFormatter:
    def format(self, text):
        return text.lower()
class UpperFormatter(TextFormatter):
    def format(self, text):
        return text.upper()
print(UpperFormatter().format("hello"))


class Message:
    def show(self):
        print("Default message")
class WelcomeMessage(Message):
    def show(self):
        print("Welcome to the system!")
WelcomeMessage().show()


class Calculator:
    def calculate(self, x, y):
        return x+y
class AdvancedCalculator(Calculator):
    def calculate(self, x, y):
        return x*y
print(AdvancedCalculator().calculate(5, 3))