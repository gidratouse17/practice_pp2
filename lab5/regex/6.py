# Write a Python program to replace all occurrences of space, comma, or dot with a colon

import re
t = input()
x = re.sub('[ ,.]', ':', t)
print(x)