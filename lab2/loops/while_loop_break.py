#1
while True:
    my_fav_fruit = input("Guess my fav fruit: ")
    if my_fav_fruit == "Banana":
        print("You got it")
        break

#2
pony = "Twilight" 
i = 0

while i < len(pony):
    if pony[i] in "aeiou":
        print("First vowel:", pony[i])
        break
    i+=1

#3
i = 0
while i != 4:
    print(i)
    if i ==3:
        break
    i+=1

#4
while True:
    number_of_room = input("I live in the room number: ")
    if number_of_room == "613":
     print("Welcome my dear friend")
     break
    print("Oh sorry, I mixed up")

#5
k = 9
while k > 0:
    print(k)
    if k % 2 ==0:
        break
    k-=3