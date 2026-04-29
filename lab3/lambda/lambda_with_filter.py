#1
nums = [9, 11, 12, 33, 68, 72]
res = list(filter(lambda x: x % 2 == 0, nums))
print(res)

#2
names = ["Akezhan", "Abilseiit", "Nurdana", "Diana"]
a = list(filter(lambda x: x.startswith("A"), names))
print(a)

#3
students = [
    {"name": "Dariga", "gpa": 2.33},
    {"name": "Sasha", "gpa": 1.50},
    {"name": "Askhat", "gpa": 3.33}
]
high = list(filter(lambda g: g["gpa"] > 3.00, students))
print(high)
#4
wods = ["Blue", "Goodbye", "bro", "no"]
ay= list(filter(lambda x: len(x) > 4, wods))
print(ay)