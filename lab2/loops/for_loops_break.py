#1
for i in range(1, 99):
    if i == 5:
        break
    print(i)

#2
characters = ["Piper", "Jessie", "Bea", "Max"]

for name in characters:
    if name == "Bea":
        print("Ill play Bea today")
        break

#3
for _ in range(3):
    answer = input("Now spell answer: ")
    if answer == "freedom":
        print("Correct!")
        break
else:
    print("You lost.")

#4
my_word = "sparkle"

for ch in my_word:
    if ch == "l":
        print("Found l")
        break
    print(ch)

#5
nums = [3, 5, 6, 7]

for n in nums:
    if n % 2 == 0:
        print("Even found")
        break
else:
    print("No even numbers")