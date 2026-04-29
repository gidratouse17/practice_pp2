#1
nums = [6, 12, 24, 48]
res = list(map(lambda y: y // 2, nums))
print(res)

#2
sm_wrds = ["Table", "Book", "iPhone"]
rs = list(map(lambda g : g.upper(), sm_wrds))
print(rs)

#3
fst_name = ["Karina", "Yoichi", "Pinkie"]
lst_name = ["Karzhaubaeva", "Isagi", "Pie"]

result = list(map(lambda a, b: a + " " + b, fst_name, lst_name))
print(result)
#4
k = [6, 7, 8]
o = [6, 9, 8]
rt= list(map(lambda t, u: t ==u, k, o))
print(rt)