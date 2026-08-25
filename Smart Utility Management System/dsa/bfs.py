from collections import deque

def bfs_outage(graph, affected_area):
    # Find all areas affected by outage starting from affected_area
    visited = set()
    queue   = deque([affected_area])
    visited.add(affected_area)
    affected = []

    while queue:
        current = queue.popleft()
        affected.append(current)

        for neighbor, weight in graph.get_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return affected