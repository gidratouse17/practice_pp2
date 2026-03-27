from functools import reduce
#1
even = [12, 34, 56, 78]
n = list(map(lambda x: x // 2, even))
print(n)

#2
names = ["Nurdana", "Karina", "Adelina", "Sasha", "Ali", "Alisa"]
f = list(filter(lambda k: len(k) > 5, names))
print(f)

#3
K = ["What is the", "meaning of", "my life?"]
s = reduce(lambda x, y: x + " " + y, K)
print(s)

#4 
l = [3, 5, 7]
h = list(map(lambda m: m**2, l))
print(h)

#5
words = ["Aubrey", "Apple", "Sunny", "Orange Joe", "Leave"]
r = list(filter(lambda u: u.startswith("O"), words))
print(r)