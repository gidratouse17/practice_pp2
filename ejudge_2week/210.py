n = int(input())
num = list(map(int,input().split()))

sort_num = sorted(num,reverse=True)
print(*(sort_num))