n = 6
graph = {}
graph[1] = [2, 4]
graph[2] = [3, 4]
graph[3] = [6]
graph[4] = [5]
graph[5] = [3, 6]
graph[6] = []
# n = 4
# graph = {}
# graph[1] = [4]
# graph[2] = []
# graph[3] = [2]
# graph[4] = [2, 3]
graph_copy = graph.copy()

states = []
UNWATCHED = "unwatched"
WATCHED = "watched"
USED = "used"
for _ in range(n):
    states.append(UNWATCHED)

pos = 1
ans = []
prev = []
while len(ans) != n:
    if pos == None:
        pos = prev.pop()
    vertexes = graph[pos]
    if len(vertexes) == 0:
        states[pos-1] = USED
        ans.append(pos)
        pos = None
    else:
        next_pos = None
        while len(vertexes) != 0:
           local_pos = vertexes[0]
           vertexes.remove(local_pos)
           if states[local_pos-1] != USED:
               next_pos = local_pos
               break
        if next_pos != None:
            states[pos-1] = WATCHED
            prev.append(pos)
            pos = next_pos
        else:
            states[pos-1] = USED
            ans.append(pos)
            pos = None

print(ans)



