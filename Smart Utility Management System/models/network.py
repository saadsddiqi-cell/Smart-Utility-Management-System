from dsa.graph import Graph
from dsa.dijkstra import dijkstra
from dsa.bfs import bfs_outage

# Build Karachi utility network
def build_karachi_network():
    g = Graph()

    # Add connections (area1, area2, distance in km)
    g.add_edge("Clifton",         "Defence",         3)
    g.add_edge("Defence",         "Korangi",         8)
    g.add_edge("Clifton",         "Saddar",          5)
    g.add_edge("Saddar",          "Gulshan",         7)
    g.add_edge("Saddar",          "Nazimabad",       9)
    g.add_edge("Gulshan",         "North Nazimabad", 4)
    g.add_edge("Gulshan",         "Korangi",         10)
    g.add_edge("Nazimabad",       "North Nazimabad", 3)
    g.add_edge("Nazimabad",       "Malir",           12)
    g.add_edge("Korangi",         "Malir",           6)
    g.add_edge("North Nazimabad", "Malir",           15)
    g.add_edge("Defence",         "Clifton",         3)

    return g

# Find shortest supply route
def find_shortest_route(from_area, to_area):
    g    = build_karachi_network()
    path, distance = dijkstra(g, from_area, to_area)
    return path, distance

# Find affected areas during outage
def find_affected_areas(area):
    g        = build_karachi_network()
    affected = bfs_outage(g, area)
    return affected

# Get all areas for dropdown
def get_all_areas():
    g = build_karachi_network()
    return g.get_all_nodes()