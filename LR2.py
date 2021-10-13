import numpy as np
import scipy.optimize

def not_int_pos_ordinal(x):
    pos = 0
    for num in x:
        if num - int(num) != 0:
            return pos
        pos += 1
    return pos

def not_int_pos(x):
    result_pos = 0
    pos = 0
    for num in x:
        if num - int(num) != 0:
            result_pos = pos
        pos += 1
    return result_pos

def get_Jb(result):
    x = result.x
    Jb = []
    pos = 0
    for num in x:
        if num != 0. :
            Jb.append(pos)
        pos += 1
    return Jb

def get_Jnb(result):
    x = result.x
    Jnb = []
    pos = 0
    for num in x:
        if num == 0 :
            Jnb.append(pos)
        pos += 1
    return Jnb

def get_k(result):
    k = not_int_pos(result.x)
    return k

def get_Ab(A, Jb):
    Ab = []
    for line in A:
        new_line = []
        for i in range(0, len(line)):
            if i in Jb:
                new_line.append(line[i])
        Ab.append(new_line)
    Ab = np.array(Ab)
    return Ab

def get_Anb(Anb, Jnb):
    return get_Ab(Anb, Jnb)

def make_zero_column(A):
    size = len(A)
    column = []
    for i in range(0, size):
        column.append([0])
    column = np.array(column)
    A = np.hstack([A, column])
    return A

def add_line(A, line, Jnb):
    size = len(A[0])
    column = []
    for i in range(0, size):
        column.append(0)
    for i in range(0, len(Jnb)):
        column[Jnb[i]] = line[i]
    column[len(column)-1] = -1
    column = np.array(column)
    A = np.vstack([A, column])
    return A

def add_b(b, result, k):
    b_val = result.x[k]
    b_val -= int(b_val)
    b_val = np.array([[b_val]])
    b = np.hstack([b, b_val])
    return b

def add_c(c):
    c_val = np.array([[0]])
    c = np.vstack([c, c_val])
    return c



# n = 3
# c = np.array([[-21],
#               [-11],
#               [0]])
# A_eq = np.array([[7, 4, 1]])
# b_eq = np.array([[13]])
# A_ub = np.array([[-1, 0, 0],
#                  [0, -1, 0],
#                  [0, 0, -1]])
# b_ub = np.array([[0],
#                  [0],
#                  [0]])

n = 4
c = np.array([[1],
              [-2],
              [0],
              [0]])
A_eq = np.array([[-4, 6, 1, 0],
                 [1,  1, 0, 1]])
b_eq = np.array([[9,  4]])
A_ub = np.array([[-1, 0,  0,  0],
                 [0, -1,  0,  0],
                 [0,  0, -1,  0],
                 [0,  0,  0, -1]])
b_ub = np.array([[0],
                 [0],
                 [0],
                 [0]])

Jb = []
x = []
ans = None

result = scipy.optimize.linprog(c=c, A_eq=A_eq, b_eq=b_eq, method='simplex')
if(result.success):
    Jb = get_Jb(result)
    Jnb = get_Jnb(result)
    k = get_k(result)
    print("------ k --------")
    print(k+1)
    if k >= len(result.x):
        x = result.x
        ans = -result.fun
    else:
        Ab = get_Ab(A_eq, Jb)
        print("\n------ Ab -------")
        print(str(Ab))
        Ab_inv = np.linalg.inv(Ab)
        Anb = get_Anb(A_eq, Jnb)
        Lm = np.dot(Ab_inv, Anb)
        print("\n------ Lm -------")
        print(str(Lm))
        line = Lm[k]
        c = add_c(c)
        A_eq = make_zero_column(A_eq)
        A_eq = add_line(A_eq, line, Jnb)
        b_eq = add_b(b_eq, result, k)

#return line to valid state
c = -c

print("\n------- b -------")
print(b_eq)
print("\n------- A -------")
print(A_eq)
print("\n------- C -------")
print(c)




# print()
# print("----------------------------------------------------------------------")
# print()

# print("Result:")
# if ans:
#     print("    " + str(x))
#     print("    " + str(ans))
# else:
#     print("    There is no valid integer solutions")