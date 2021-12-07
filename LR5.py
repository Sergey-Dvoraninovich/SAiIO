import copy


# def build_peaks_from_edges(peaks_list, edges):
#     peaks = {}
#     for peak in peaks_list:
#         peaks[peak] = []
#     for edge in edges:
#         peaks[edge[0][0]].append(edge[0][1])
#     return peaks


class Edge:
    def __init__(self, peak_from, peak_to, max_flow):
        self.peak_from = peak_from
        self.peak_to = peak_to
        self.current_flow = 0
        self.max_flow = max_flow

    def __str__(self):
        return 'Edge[({}, {}), {}/{}]'.format(self.peak_from, self.peak_to, self.current_flow, self.max_flow)


class SupportNetwork:
    def __init__(self, parent_graph, parent_edges, parent_reverse_edges):
        self.parent_edges = parent_edges
        self.parent_reverse_edges = parent_reverse_edges
        self.parent_graph = parent_graph
        self.graph = dict()

        for peak, neighbours in parent_graph.items():
            self.graph[peak] = []

            for edge in neighbours:
                reverse_edge = find_reverse_edge(parent_edges, parent_reverse_edges, edge)
                support_edge_max_flow = edge.max_flow - edge.current_flow + reverse_edge.current_flow
                support_edge = Edge(edge.peak_from, edge.peak_to, support_edge_max_flow)
                self.graph[peak].append(support_edge)

    def find_path(self, s, t):
        stack = [s]
        peaks_marks = [(False, None) for _ in self.graph.keys()]
        peaks_marks[s] = True, None

        while len(stack) != 0:
            peak = stack.pop()

            for edge in self.graph[peak]:
                if edge.max_flow != 0 and not peaks_marks[edge.peak_to][0]:
                    stack.append(edge.peak_to)
                    peaks_marks[edge.peak_to] = True, edge.peak_from

        if peaks_marks[t] == None:
            return None

        peak_path = []
        current_peak = t

        while current_peak != None:
            peak_path.append(current_peak)
            current_peak = peaks_marks[current_peak][1]

        peak_path.reverse()
        edge_path = []

        if len(peak_path) > 1:
            out_path = copy.deepcopy(peak_path)
            result = "Path " + str(out_path.pop(0))
            for peak in out_path:
                result += "-" + str(peak)
            print(result, end='')

        for i in range(1, len(peak_path)):
            peak_1 = peak_path[i - 1]
            peak_2 = peak_path[i]
            edge = list(filter(lambda arc: arc.peak_to == peak_2, self.graph[peak_1]))[0]
            edge_path.append(edge)

        if len(edge_path) == 0:
            return None

        return edge_path

    def update_network(self, edge_path):
        for edge in edge_path:
            reverse_edge = find_reverse_edge(self.parent_edges, self.parent_reverse_edges, edge)

            support_edge_max_flow = edge.max_flow - edge.current_flow + reverse_edge.current_flow
            support_edge = self.find_arc(edge.peak_from, edge.peak_to)
            support_edge.max_flow = support_edge_max_flow
            edges = self.graph[edge.peak_from]
            edges[edges.index(support_edge)] = support_edge

            reverse_support_edge_max_flow = reverse_edge.max_flow - reverse_edge.current_flow + edge.current_flow
            reverse_support_edge = self.find_arc(edge.peak_to, edge.peak_from)
            reverse_support_edge.max_flow = reverse_support_edge_max_flow
            edges = self.graph[edge.peak_to]
            edges[edges.index(reverse_support_edge)] = reverse_support_edge


    def find_arc(self, vertex_1, vertex_2):
        arcs = self.graph[vertex_1]

        return list(filter(lambda arc: arc.peak_to == vertex_2, arcs))[0]


def find_max_flow(graph, edges, reversed_edges, start_peak, finish_peak):
    result_flow = 0
    support_network = SupportNetwork(graph, edges, reverse_edges)

    while True:
        support_edges = support_network.find_path(start_peak, finish_peak)

        if support_edges == None:
            break

        flow = min(map(lambda edge: edge.max_flow, support_edges))
        print(' Flow', flow)
        result_flow += flow
        path_edges = to_edges(graph, support_edges)
        not_path_edges = list(set(edges + reverse_edges) - set(path_edges))

        for edge in path_edges:
            rev_current_flow = find_reverse_edge(edges, reverse_edges, edge).current_flow
            edge.current_flow = max(0, edge.current_flow - rev_current_flow + flow)

        for edge in not_path_edges:
            fp_a_reversed = flow if find_reverse_edge(edges, reverse_edges, edge) in path_edges else 0
            rev_current_flow = find_reverse_edge(edges, reverse_edges, edge).current_flow
            edge.current_flow = max(0, edge.current_flow - rev_current_flow - fp_a_reversed)

        support_network.update_network(path_edges)

    return result_flow


def find_reverse_edge(edges, reverse_edges, edge):
    if edge not in edges:
        edge_index = reverse_edges.index(edge)
        reverse_edge = edges[edge_index]
    else:
        edge_index = edges.index(edge)
        reverse_edge = reverse_edges[edge_index]

    return reverse_edge


def to_edges(graph, support_edges):
    edges = []

    for support_edge in support_edges:
        search_edges = graph[support_edge.peak_from]
        edge = list(filter(lambda edge: edge.peak_to == support_edge.peak_to, search_edges))[0]
        edges.append(edge)

    return edges

n = 4
edges_data = {
    (0, 1): 3, (0, 2): 2,
    (1, 2): 2, (1, 3): 1,
    (2, 3): 2
}

graph = dict()
edges = []
reverse_edges = []

for i in range(0, n):
    graph[i] = []

for from_to in edges_data.keys():
    edge = Edge(from_to[0], from_to[1], edges_data[from_to])
    edges.append(edge)
    graph[from_to[0]].append(edge)

for edge in edges:
    edge_reversed = Edge(edge.peak_to, edge.peak_from, 0)
    graph[edge.peak_to].append(edge_reversed)
    reverse_edges.append(edge_reversed)

print('\nResult flow is ', find_max_flow(graph, edges, reverse_edges, 0, n-1))

