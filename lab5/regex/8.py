# Write a Python program to split a string at uppercase letters

import re
t = input()
x = re.split('(?=[A-Z])', t)
print(x)