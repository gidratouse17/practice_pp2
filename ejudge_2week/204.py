x = int(input())
num = list(map(int, input().split()))
countt = 0
for i in num:
    if i>0:
        countt+=1
print(countt)