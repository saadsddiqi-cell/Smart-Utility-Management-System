class Graph:
    def __init__(self):
        # Adjacency list — stores connections
        self.nodes = {}

    # Add area to graph
    def add_node(self, area):
        if area not in self.nodes:
            self.nodes[area] = []

    # Add connection between two areas with weight
    def add_edge(self, area1, area2, weight):
        self.add_node(area1)
        self.add_node(area2)
        self.nodes[area1].append((area2, weight))
        self.nodes[area2].append((area1, weight))

    # Get all neighbors of an area
    def get_neighbors(self, area):
        return self.nodes.get(area, [])

    # Get all areas
    def get_all_nodes(self):
        return list(self.nodes.keys())

    # Display graph
    def display(self):
        for area, neighbors in self.nodes.items():
            print(f"{area} → {neighbors}")