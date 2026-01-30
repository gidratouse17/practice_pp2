import sys
print(sys.version)
ps4_games = ["Spongebob", "It takes 2", "Uncharted"]
ps4_games.append("Detroit")    #we're adding this in the end
ps4_games.sort()      #sort by alphabet
print("My fav ps4 games", ps4_games)

junk_food = ["Burger", "Doner", "Pelmeni"]
junk_food.pop()     #deleting the last element
print("Don't eat:", junk_food)

import random
wanna_skip = ["English", "Sociology", "Kazakh"]
print("Today I'll skip", random.choice(wanna_skip))

my_username = "krzhbv_k"
if len(my_username) > 6:
 print("Check my tg:", my_username)
else:
 print("Noooo, that's not my username")
