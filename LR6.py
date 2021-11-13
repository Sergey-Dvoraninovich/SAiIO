import numpy as np
import bisect

class PeakInfo:
    def __init__(self, name, prev_name, path, is_watched):
        self.name = name
        self.prev_name = prev_name
        self.path = path
        self.is_watched = is_watched

    def __lt__(self, other):
        if self.is_watched == other.is_watched:
            if self.path < other.path:
                result = True
            else:
                result = False
        elif self.is_watched and not other.is_watched:
            result = False
        elif not self.is_watched and other.is_watched:
            result = True
        return result

    def __str__(self):
        return '(peak {}, path {}, is wathced {})'.format(self.name, self.path, self.is_watched)

def build_peaks_outputs_from_edges(peaks_list, edges_dict):
    peaks = {}
    for peak in peaks_list:
        peaks[peak] = []
    edges_keys = edges_dict.keys()
    for edge in edges_keys:
        peaks[edge[0]].append(edge[1])
    return peaks

def paths_info(processed_list, start):
    prev_dict = {}
    paths_info_lines = []
    for peak_info in processed_list:
        prev_dict[peak_info.name] = peak_info.prev_name
    for peak_info in processed_list:
        path_peaks = []
        current_peak = peak_info.name
        while current_peak != None:
            path_peaks.append(current_peak)
            current_peak = prev_dict[current_peak]
        path_line = ""
        path_peaks = path_peaks[::-1]
        for peak in path_peaks:
            path_line += " - " + peak
        path_line = path_line[3:]
        paths_info_lines.append([path_line, peak_info.path])
    return paths_info_lines


peaks_list = ['V_1', 'V_2', 'V_3', 'V_4']
start = 'V_1'
finish = 'V_4'
edges = {}
edges[('V_1', 'V_2')] = 1
edges[('V_1', 'V_3')] = 4
edges[('V_2', 'V_3')] = 2
edges[('V_3', 'V_2')] = 3
edges[('V_3', 'V_4')] = 1
peaks_outputs = build_peaks_outputs_from_edges(peaks_list, edges)

processing_list = [PeakInfo(start, None, 0, False)]
for peak in peaks_list:
    if peak != start:
        processing_list.append(PeakInfo(peak, None, np.inf, False))

processed_amount = 0
while processed_amount < len(peaks_list):
    current_item = processing_list.pop(0)
    current_item.is_watched = True
    bisect.insort(processing_list, current_item)

    next_peaks_names = peaks_outputs[current_item.name]

    for next_peak_name in next_peaks_names:
        next_item = list(filter(lambda x: x.name == next_peak_name, processing_list))[0]
        if current_item.path + edges[(current_item.name, next_item.name)] < next_item.path:
            processing_list.remove(next_item)
            next_item.path = current_item.path + edges[(current_item.name, next_item.name)]
            next_item.prev_name = current_item.name
            bisect.insort(processing_list, next_item)

    processed_amount += 1

paths_info_lines = paths_info(processing_list, start)
for info in paths_info_lines:
    print("{} total coast: {}".format(info[0], info[1]))

