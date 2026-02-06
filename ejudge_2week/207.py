n = int(input())
num = list(map(int, input().split()))
max_val = num[0]
pos = 1

for i in range(len(num)):
    if num[i] > max_val:
        max_val = num[i]
        pos = i + 1
print(pos)