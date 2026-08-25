import heapq

def dijkstra(graph, start, end):
    # Distance from start to all nodes
    distances = {node: float('inf') for node in graph.get_all_nodes()}
    distances[start] = 0

    # Previous node in shortest path
    previous = {node: None for node in graph.get_all_nodes()}

    # Priority queue — (distance, node)
    pq = [(0, start)]

    visited = set()

    while pq:
        current_dist, current_node = heapq.heappop(pq)

        if current_node in visited:
            continue
        visited.add(current_node)

        # Stop if we reached destination
        if current_node == end:
            break

        # Check all neighbors
        for neighbor, weight in graph.get_neighbors(current_node):
            distance = current_dist + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))

    # Build path
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = previous[current]
    path.reverse()

    # Return path and total distance
    if distances[end] == float('inf'):
        return [], -1  # no path found

    return path, distances[end]