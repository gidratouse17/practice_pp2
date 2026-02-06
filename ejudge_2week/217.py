n = int(input())

cnt = {}

for _ in range(n):
    phone = input()
    if phone in cnt:
        cnt[phone] += 1
    else:
        cnt[phone] = 1

answer = 0
for v in cnt.values():
    if v == 3:
        answer += 1

print(answer)

