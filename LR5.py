import copy


def build_peaks_from_edges(peaks_list, edges):
    peaks = {}
    for peak in peaks_list:
        peaks[peak] = []
    for edge in edges:
        peaks[edge[0][0]].append(edge[0][1])
    return peaks

def find_path(peaks, start, finish):
    path = []
    stack = []
    current_item = start

    while (current_item != finish):
        current_line = copy.deepcopy(peaks[current_item])
        current_line = current_line[::-1]

        for item in current_line:
            stack.append((item, current_item))

        if len(stack) == 0:
            path = None
            break

        full_item = stack.pop(len(stack)-1)
        current_item = full_item[0]

        #if len(current_line) == 0:
        #    while(current_item)

        path.append(full_item)

    return path





peaks_list = ['A', 'B', 'C', 'D', 'E', 'F']
start = 'A'
finish = 'F'
init_edges = [[('A', 'B'), 3],
              [('A', 'C'), 2],

         [('B', 'E'), 1],
         #[('B', 'C'), 2],

         #[('C', 'E'), 1],
         [('C', 'D'), 2],

         #[('E', 'F'), 1],
         #[('E', 'D'), 2],

         [('D', 'F'), 2]]
init_peaks = build_peaks_from_edges(peaks_list, init_edges)


edges = copy.deepcopy(init_edges)
peaks = copy.deepcopy(init_peaks)
while True:
   path = find_path(peaks, start, finish)

