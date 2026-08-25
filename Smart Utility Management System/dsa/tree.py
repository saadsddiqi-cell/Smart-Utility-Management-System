class TreeNode:
    def __init__(self, name, node_type="area", data=None):
        self.name      = name
        self.node_type = node_type  # "city", "zone", "area"
        self.data      = data or {}
        self.children  = []

    def add_child(self, child_node):
        self.children.append(child_node)

    def is_leaf(self):
        return len(self.children) == 0


class CityTree:
    def __init__(self):
        self.root = None

    def build_karachi_tree(self):
        # Root — City
        self.root = TreeNode("Karachi", "city")

        # Zone North
        zone_north = TreeNode("Zone North", "zone")
        zone_north.add_child(TreeNode("Nazimabad",       "area", {"electricity": 72, "water": 65, "gas": 80}))
        zone_north.add_child(TreeNode("North Nazimabad", "area", {"electricity": 68, "water": 70, "gas": 75}))
        zone_north.add_child(TreeNode("Gulshan",         "area", {"electricity": 85, "water": 78, "gas": 82}))

        # Zone South
        zone_south = TreeNode("Zone South", "zone")
        zone_south.add_child(TreeNode("Clifton", "area", {"electricity": 90, "water": 88, "gas": 70}))
        zone_south.add_child(TreeNode("Defence", "area", {"electricity": 95, "water": 85, "gas": 68}))
        zone_south.add_child(TreeNode("Saddar",  "area", {"electricity": 78, "water": 72, "gas": 85}))

        # Zone East
        zone_east = TreeNode("Zone East", "zone")
        zone_east.add_child(TreeNode("Korangi", "area", {"electricity": 65, "water": 60, "gas": 72}))
        zone_east.add_child(TreeNode("Malir",   "area", {"electricity": 60, "water": 55, "gas": 68}))

        # Add zones to root
        self.root.add_child(zone_north)
        self.root.add_child(zone_south)
        self.root.add_child(zone_east)

        return self.root

    # Pre-order traversal — Root → Left → Right
    def preorder(self, node, result=None):
        if result is None:
            result = []
        if node:
            result.append({
                "name"     : node.name,
                "type"     : node.node_type,
                "data"     : node.data,
                "children" : len(node.children)
            })
            for child in node.children:
                self.preorder(child, result)
        return result

    # Get tree as nested dict for JSON
    def to_dict(self, node=None):
        if node is None:
            node = self.root
        return {
            "name"     : node.name,
            "type"     : node.node_type,
            "data"     : node.data,
            "children" : [self.to_dict(child) for child in node.children]
        }

    # Search for a node by name
    def search(self, name, node=None):
        if node is None:
            node = self.root
        if node.name == name:
            return node
        for child in node.children:
            result = self.search(name, child)
            if result:
                return result
        return None

    # Get all areas (leaf nodes)
    def get_all_areas(self, node=None, areas=None):
        if node is None:
            node = self.root
        if areas is None:
            areas = []
        if node.is_leaf():
            areas.append(node)
        for child in node.children:
            self.get_all_areas(child, areas)
        return areas