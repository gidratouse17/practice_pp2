#1
def newton_sec_law(mass, acceleration):
  return(mass * acceleration)

print(newton_sec_law(5, 10))
print(newton_sec_law(6, 7))   

#2
def i_miss_my_home():
  return "I wanna go back"

message = i_miss_my_home()
print(message)

#3
def sleepy_time():
  return "Go to rest, sleep well"

print(sleepy_time())


#4
def is_int(value):
   if isinstance(value, int):
      return "It is integer"
   else:
      return "Its not integer"
   
print(is_int(5))
print(is_int("Hypotenuse"))
print(is_int(3.14))   



