# Write a Python program to convert snake case string to camel case string

import re
t = input()
x = re.sub('_(\w)', lambda m: m.group(1).upper(), t)
print(x)