#1
def surn_name(namee):  #namee is a parameter
  print(namee + "Thunderman")

surn_name("Phoebe")  #phoebe, max, nora are arguments
surn_name("Max")
surn_name("Nora") 

#2
def fav_hobbies(hobby):
  print("I have my most fav hobby: ", hobby)

fav_hobbies(hobby = "collectioning figures")  #keyword arg

#3
def fruitss(fruit = "peaches"):  #default value
  print("I love", fruit)

fruitss("bananas")
fruitss("orange")
fruitss()
fruitss("apples")

#4
def my_friend(animal, name):
  print("I have a", animal)
  print("My", animal + "'s name is", name)

my_friend("cat", "Poti")  #positional arg

