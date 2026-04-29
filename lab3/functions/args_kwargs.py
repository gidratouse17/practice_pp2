#1
def our_group(*person):
  print("The oldest one is " + person[1])

our_group("Karina", "Ina", "Katya")


#2
def my_function(farewell, *names):
  for name in names:
    print(farewell, name)

my_function("Goodbye,", "Askhat", "Dariga", "Aziza")

#3
def show_info(**data):
  print(data)

show_info(name = "Twilight", age = "27") 

#4
def blue_lock(name, *abilities, **info):
  print("Character:", name)
  print("Ability:", abilities)
  print("Extra info:", info)

blue_lock(
    "Chigiri Hyoma",
    "Speed",
    "Concentration",
    fav_animal = "black cat",
    trauma = "rasryv perednei svyazki"
  )
