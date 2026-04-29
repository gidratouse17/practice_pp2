#1
k = lambda x : x + 12
print(k(48))

#2
mx_num = lambda x, y: x if x > y else y
print(mx_num(10, 9))

#3
together = lambda o, p: o + " " + p
print(together("Automation", "is the best"))

#4
boool = lambda y: y >= 150
print(boool(22))

#5
def myfunc(n):
  return lambda a : a * n

numbers = [4, 6, 7, 9]

mult_fourr= myfunc(4)

for num in numbers:
  print(mult_fourr(num))