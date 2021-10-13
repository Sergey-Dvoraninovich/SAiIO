import numpy as np

n = 3
Q = 3 + 1

A = [[0, 1, 2, 3],
     [0, 0, 1, 2],
     [0, 2, 2, 3]]

opt = []
x = []
for _ in range(n):
    opt_line = []
    x_line = []
    for _ in range(Q):
        opt_line.append(0)
        x_line.append(0)
    opt.append(opt_line)
    x.append(x_line)

opt[0][0] = A[0][0]
x[0][0] = 0
for i in range(Q):
    if A[0][i] > opt[0][i-1]:
        opt[0][i] = A[0][i]
        x[0][i] = i
    else:
        opt[0][i] = opt[0][i-1]
        x[0][i] = x[0][i-1]

for k in range(1, n):
    for q in range(0, Q):
        max = A[k][q]
        max_pos = q
        for i in range(0, q):
            value = opt[k-1][q-i] + A[k][i]
            if value > max:
                max = value
                max_pos = i
        opt[k][q] = max
        x[k][q] = max_pos

seller_goods = []
current_amount = Q - 1
q = Q - 1
k = n - 1
while current_amount != 0:
    amount = x[k][q]
    seller_goods.append([k+1, amount])
    current_amount -= amount
    if (amount == 0):
        q -= 1
    k -= 1
seller_goods = sorted(seller_goods, key=lambda x: x[0])

print("------- OPT -------")
print(np.array(opt))
print("-------- X --------")
print(np.array(x))
print("seller | goods amount")
for item in seller_goods:
    print("  " + str(item[0]) + "           " + str(item[1]))