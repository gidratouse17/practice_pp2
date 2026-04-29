# 1. Write a Python program to convert degree to radian.

import math
a = float(input("Input degree: "))
b = a*math.pi/180
print("Output radian: ", b)

import math
a = float(input("Input degree: "))
print("Output radian: ", math.radians(a))


# 2. Write a Python program to calculate the area of a trapezoid.

import math
h = int(input("Height: "))
a = int(input("Base, first value: "))
b = int(input("Base, second value: "))

print((a+b)/2 * h)



# 3. Write a Python program to calculate the area of regular polygon.

import math
n = int(input("Input number of sides: "))
l = int(input("Input the length of a side: "))
S = (n * math.pow(l, 2)) / (4 * math.tan(math.pi/n))
print("The area of polygon is: ", int(S))



# 4. Write a Python program to calculate the area of a parallelogram.

import math
l = int(input("Length of base: "))
h = int(input("Height of parallelogram: "))
S = float(l * h)
print(S)