#1
n = [44, 25, 56, 10]
r = sorted(n, key = lambda p: p % 10) #sort with last number
print(r)

#2
names = ["Saniya", "Boris", "Nurdana", "Kamila"]
re = sorted(names, key = lambda r: r[0])
print(re)
#3
vege = ["potato", "luk", "cucumber"]
v = sorted(vege, key=lambda x: len(x))
print(v)

#4
rnd = ["book", "chocolate", "magnum", "cat"]
i= sorted(rnd, key=lambda k: k[-1])
print(i)
