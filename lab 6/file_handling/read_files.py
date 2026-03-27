#1 first way to read file
monster = open('bachira.txt', 'r')
inside = monster.read()
print(inside)
monster.close()

#2 second (more safe) way to read file
with open('isagi.txt', 'r') as safe:
    code = safe.read()
    print(code)

#3  read only first and second line
with open('omori.txt', 'r') as snuuy:
    line1 = snuuy.readline()
    line2 = snuuy.readline()

print("First line:", line1.strip())
print("Second line:", line2.strip())

#4 print 1 symbol
with open('omori.txt', 'r') as mari:
    l1 = mari.readline()
    l2 = mari.readline()

print(l2[2])