#1
words = ["meal", "adventure", "hi", "twilight", "sun"]
i = 0

while i < len(words):
    word = words[i]
    i += 1

    if len(word) < 4:
        continue

    print("Long word:", word)

#2
while True:
    password = input("Enter password: ")

    if password == "1234":
        print("Try something else")
        continue

    print("Password accepted")
    break

#3
nums = [9, -123, 56]
i = 0
while i < len(nums):
    if nums[i] < 0:
        i += 1
        continue
    print(nums[i])
    i += 1


#4
while True:
    p = input(": ")
    if len(p) < 6:
        continue
    print("ok")
    break

#5
while True:
    answer = input("Do you agree with this statement? (Yes/No): ")

    if answer != "Yes" and answer != "No":
        print("Wrong answer")
        continue

    print("Answer saved:", answer)
    break
