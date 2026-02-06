n = int(input())
num = list(map(int, input().split()))
max = -99999999
for i in num:
    if i > max:
        max = i
print(max) 