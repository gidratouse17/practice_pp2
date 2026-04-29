# Create a generator that generates the squares of numbers up to some number N.

def gen(a):
    for i in range(1, a):
        yield i**2
a = int(input())
sqgen = gen(a)
for num in sqgen:
    print(num)

# Write a program using generator to print the even numbers between 0 and n in comma separated form where n is input from console.

def gen(a):
    for i in range(0, a+1, 2):
        yield i
a = int(input())
even = gen(a)
for ev in even:
    print(ev)


# Define a function with a generator which can iterate the numbers, which are divisible by 3 and 4, between a given range 0 and n.

def gen(n):
    for i in range(0, n+1):
        if i % 3 == 0 and i % 4 == 0:
            yield i
n = int(input())
for num in gen(n):
    print(num)


# Implement a generator called squares to yield the square of all numbers from (a) to (b). Test it with a "for" loop and print each of the yielded values.

def gen(a, b):
    for i in range(a, b+1):
        yield i**2
a = int(input())
b = int(input())
for even in gen(a, b):
    print(even)


# Implement a generator that returns all numbers from (n) down to 0.

def gen(a):
    for i in range(a, -1, -1):
        yield i
a = int(input())
for num in gen(a):
    print(num)