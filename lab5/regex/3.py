# Write a Python program to find sequences of lowercase letters joined with a underscore

import re
t = input()
x = re.findall('[a-z]+_[a-z]+', t)
print(x)