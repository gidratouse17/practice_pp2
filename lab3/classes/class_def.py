#1
# A Class is like an object constructor, or a "blueprint" for creating objects.

class MyClass:
  x = 5
p1 = MyClass()
print(p1.x)
del p1


class Dog:
    species = "Shiba inu"
my_dog = Dog()
print(my_dog.species)

class Dog:
    def bark(self):
        print("Woof!")
dog = Dog()
dog.bark()


class Animal():
    wild_animal = "Wolves"
animal1 = Animal()
print(animal1.wild_animal)