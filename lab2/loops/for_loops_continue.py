#1
for i in range(8):
    if i == 5:
        continue
    print(i, end = " ")

print()
#2
another_word = "piper"

for ch in another_word:
    if ch == "p":
        continue
    print(ch, end= "")
print()

#3
characters = ["Spongebob", "Patrick", "Squidward", "Pearl", "Plankton"]

for name in characters:
    if name == "Pearl":
        continue
    print(name)

#4
for i in range(1, 15):
    if i % 2 == 0:
        continue
    print(i, end= " ")
   
print()

#5
text = "i love fit25bd"

for cha in text:
    if cha == " ":
        continue
    print(cha, end= "")
