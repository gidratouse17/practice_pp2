#1 what 'w' do
with open('plans_summer.txt', 'w') as file:
    file.write("I want to visit my relatives")

with open('plans_summer.txt', 'w') as file:
    file.write("I want to stay at Aktau")


#2 what 'a' do
with open ('new_file.txt', 'w') as f:
    f.write("I want to learn piano\n")

with open('new_file.txt', 'a') as f:
    f.write("to learn how to play 'Duet' from Omori\n")

#3 create and write file with "f"
char = "Kel"
with open('sunny.txt', 'w') as friend:
    friend.write(f"I would be friends with {char}")
