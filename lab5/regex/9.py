# Write a Python program to insert spaces between words starting with capital letters

import re
t = input()
x = re.sub('([A-Z])', lambda m: ' ' + m.group(1), t).strip()
print(x)