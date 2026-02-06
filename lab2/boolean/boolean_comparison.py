#1
if 99 == 99:
    print("They are equal")
else:
    print("Its false")

    #2
if False:
    print("It will never work")
else:
    print("Now this will work cuz its false")

#3
n = input()
if len(n) < 10:
    print("Small string")
else:
    print("Big string")
  
#4
if True:
    print("It will work since its True")
else:
    print("But else will not gonna work")

#5
num = int(input())
print(bool(num))