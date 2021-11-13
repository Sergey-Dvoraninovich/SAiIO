import numpy as np
import scipy.optimize
import copy
import math
import collections

class LP:
    def __init__(self, c, A_ub, b_ub):
        self.c = c
        self.A_ub = A_ub
        self.b_ub = b_ub

    def solve(self):
        result = scipy.optimize.linprog(c=self.c, A_ub=self.A_ub, b_ub=self.b_ub, method='simplex')
        return result


def is_valid_ans(x):
    ans = True
    for num in x:
        if num == np.inf:
            ans = False
    return ans


def not_int_pos(x):
    pos = 0
    for num in x:
        if num - int(num) != 0:
            return pos
        pos += 1
    return pos


def make_left_node(node, x, pos, n):
    local_node = copy.deepcopy(node)

    A_ub_line = []
    for i in range(0, n):
        if i == pos:
            A_ub_line.append(1)
        else:
            A_ub_line.append(0)
    A_ub_line = np.array(A_ub_line)
    local_node.A_ub = np.vstack([local_node.A_ub, A_ub_line])

    b = x[pos]
    b = math.floor(b)
    b = np.array([b])
    local_node.b_ub = np.vstack([local_node.b_ub, b])

    return local_node


def make_right_node(node, x, pos, n):
    local_node = copy.deepcopy(node)

    A_ub_line = []
    for i in range(0, n):
        if i == pos:
            A_ub_line.append(-1)
        else:
            A_ub_line.append(0)
    A_ub_line = np.array(A_ub_line)
    local_node.A_ub = np.vstack([local_node.A_ub, A_ub_line])

    b = x[pos]
    b = math.ceil(b)
    b *= -1
    b = np.array([b])
    local_node.b_ub = np.vstack([local_node.b_ub, b])

    return local_node


n = 2
ans_x = []
for i in range(0, n):
    ans_x.append(np.inf)
r = -1 * np.inf

c = np.array([[5],
              [-4]])
A_ub = np.array([[4, 3],
                 [-4, 3],
                 [-1, 0],
                 [1, 0],
                 [0, -1],
                 [0, 1]])
b_ub = np.array([[22],
                 [2],
                 [-2],
                 [4],
                 [0],
                 [5]])

LP_node = LP(c, A_ub, b_ub)
nodes = collections.deque()
nodes.append(LP_node)

while len(nodes) != 0:
    current_node = nodes.pop()
    result = current_node.solve()
    if True:
        x = result.x
        fun = result.fun
        fun *= -1
        pos = not_int_pos(x)
        if pos == n:
            if fun > r:
                ans_x = x
                r = fun
        else:
            if fun > r:
               nodes.append(make_left_node(current_node, x, pos, n))
               nodes.append(make_right_node(current_node, x, pos, n))
        print(x)
        print(ans_x)
        print(r)
        print()

print("Result:")
if is_valid_ans(ans_x):
    print("    " + str(ans_x))
    print("    " + str(r))
else:
    print("    There is no valid integer solutions")