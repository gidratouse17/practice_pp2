# Write a Python program that matches a string that has an 'a' followed by zero or more 'b'

import re
t = input()
x = re.findall('ab*', t)
print(x)