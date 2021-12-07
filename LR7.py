import networkx as nx
import numpy as np
import copy

#  Returns cycle, which starts on the destination edge point
# and finishes in the start edge point
def process_cycle(cycle_search_graph, edge):
    cycle = []
    #print('----------------')
    for local_cycle in nx.simple_cycles(cycle_search_graph):
        if (len(local_cycle)) != 2:
            cycle = local_cycle
            #print(local_cycle)
    #print('----------------')
    while not ((cycle[0] == edge[0] and cycle[-1] == edge[1])\
          or (cycle[0] == edge[1] and cycle[-1] == edge[0])):
        cycle.append(cycle[0])
        cycle.pop(0)
    if cycle[0] == edge[0] and cycle[-1] == edge[1]:
        cycle = cycle[::-1]
    return cycle

def get_B_peaks(B):
    dict = {}
    for edge in B:
        dict[edge[0]] = 0
        dict[edge[1]] = 0
    return sorted(list(dict.keys()))

def solve_linear_system(graph, B, not_B):
    equation_items = get_B_peaks(B)
    items_amount = len(equation_items)

    M_line = [0 for _ in range(items_amount)]
    M_line[equation_items.index(B[0][0])] = 1
    M = [M_line]
    V = [[0]]

    for edge in B:
        V.append([graph[edge]])
        M_line = [0 for _ in range(items_amount)]
        M_line[equation_items.index(edge[0])] = 1
        M_line[equation_items.index(edge[1])] = -1
        M.append(M_line)

    u_line = np.linalg.solve(M, V)
    u_line = np.transpose(u_line)[0]

    u_dict = {}
    for i in range(len(u_line)):
        u_dict[equation_items[i]] = u_line[i]

    deltas_dict = {}
    for edge in not_B:
        delta = u_dict[edge[0]] - u_dict[edge[1]] - graph[edge]
        deltas_dict[delta] = edge

    return deltas_dict

def solve(peaks_dict, graph, flow_graph, B, not_B):
    cycle_search_graph = nx.DiGraph()
    for edge in B:
        cycle_search_graph.add_edge(edge[0], edge[1])
        cycle_search_graph.add_edge(edge[1], edge[0])

    while (True):
        deltas_dict = solve_linear_system(graph, B, not_B)
        deltas = sorted(deltas_dict.keys())

        if deltas[-1] <= 0:
            return B, flow_graph

        new_edge = (6, 1)#deltas_dict[deltas[0]]
        print(new_edge)
        not_B.remove(new_edge)
        B.append(new_edge)
        cycle_search_graph.add_edge(new_edge[0], new_edge[1])
        cycle_search_graph.add_edge(new_edge[1], new_edge[0])

        cycle = process_cycle(cycle_search_graph, new_edge)

        negative_edges = []
        for i in range(1, len(cycle)):
            edge_from = cycle[i - 1]
            edge_to = cycle[i]
            local_edge = (edge_from, edge_to)
            print(local_edge)
            if graph.get(local_edge, None) is None:
                negative_edges.append(local_edge)

        print(negative_edges)
        break



graph = {}
graph[(1, 2)] = 1
graph[(6, 1)] = -2
graph[(2, 6)] = 3
graph[(3, 2)] = 3
graph[(6, 3)] = 3
graph[(6, 5)] = 4
graph[(5, 3)] = 4
graph[(3, 4)] = 5
graph[(5, 4)] = 1

peaks_dict = {}
peaks_dict[1] = 1
peaks_dict[2] = -4
peaks_dict[3] = -5
peaks_dict[4] = -6
peaks_dict[5] = 5
peaks_dict[6] = 9

B = [(1, 2), (3, 2), (6, 3), (3, 4), (5, 4)]
not_B = []
B_val = [1, 3, 9, 1, 5]

flow_graph = {}
for edge in graph.keys():
    flow_graph[edge] = 0

flow_graph = {}
for i in range(len(B)):
    flow_graph[B[i]] = B_val[i]

not_B = copy.deepcopy(graph)
for edge in B:
    not_B.pop(edge)
not_B = list(not_B.keys())

solve(peaks_dict, graph, flow_graph, B, not_B)