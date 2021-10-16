import numpy as np
from lr4_utils import sort_graph

n = 6
graph = {}
graph[1] = [2, 4]
graph[2] = [3, 4]
graph[3] = [6]
graph[4] = [5]
graph[5] = [3, 6]
graph[6] = []
graph_values = {(1, 2): 1, (1, 4): 2,
                (2, 3): 4, (2, 4): 3,
                (3, 6): 1,
                (4, 5): 5,
                (5, 3): 4, (5, 6): 2}
# n = 4
# graph = {}
# graph[1] = [4]
# graph[2] = []
# graph[3] = [2]
# graph[4] = [2, 3]


sorted_graph = sort_graph(graph, n)

graph_in = {}
for i in range(n):
    graph_in[i+1] = []
for i in range(n):
    values = graph[i+1]
    for v in values:
        graph_in[v].append(i+1)

print(graph_in)
print(sorted_graph)

range = {}
prevs = {}
for v in sorted_graph:
    value = 0
    print("----- " + str(v) + " -----")
    possible_values = []
    possible_prevs = {}
    for prev_v in graph_in[v]:
        range_val = -np.inf if range[prev_v] is None else range[prev_v]
        val = range_val + graph_values[(prev_v, v)]
        possible_prevs[val] = prev_v
        possible_values.append(range_val + graph_values[(prev_v, v)])
        print(str(range_val) + " + " + str(graph_values[(prev_v, v)]) + "   prev-" + str(prev_v))
    if len(possible_values) != 0:
       value = max(possible_values)
       prevs[v] = possible_prevs[value]
       print(value)
    range[v] = value
print("------- values -------")
print(range)

print("------- path -------")
prevs_line = ""
current_v = n
while (current_v != 1):
    prevs_line += str(current_v) + "-"
    current_v = prevs[current_v]
prevs_line += "1"
print(prevs_line)





