n = int(input())
arr = list(map(int, input().split()))

freq = {}

for x in arr:
    if x in freq:
        freq[x] += 1
    else:
        freq[x] = 1

max_count = 0
answer = None

for key in freq:
    if freq[key] > max_count:
        max_count = freq[key]
        answer = key
    elif freq[key] == max_count and key < answer:
        answer = key

print(answer)
