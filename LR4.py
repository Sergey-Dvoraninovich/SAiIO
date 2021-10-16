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
                (4, 5): 1,
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

range = {}
for v in graph_in:
    value = 0
    possible_values = []
    for prev_v in graph_in[v]:
        print(range[prev_v])
        range_val = range[prev_v] if range[prev_v] is None else - np.inf
        possible_values.append(range_val + graph_values[(prev_v, v)])
    if len(possible_values) != 0:
       value = max(possible_values)
       print(value)
    range[v] = value
print(range)





