import re

t = input()

res = re.sub(r"([A-Z])", r"_\1", t).lower()
print(res)