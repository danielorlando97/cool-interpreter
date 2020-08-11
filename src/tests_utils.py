from print_tree import print_tree


class Node:
    def __init__(self, value, parent):
        self.value = value
        self.children = []
        if parent is not None:
            parent.children.append(self)

class Print_tree(print_tree):
    def get_children(self, node):
        return node.children
    def get_node_str(self, node):
        return str(node.value)