from lark import Tree, Token
from print_tree import print_tree


def adapt_tree(node, parent=None):
    # if node is Token:
    try:
        result = Node(node.value, parent)
        return result

    # if node is Tree:
    except AttributeError:
        result = Node(node.data, parent)
        for n in node.children:
            adapt_tree(n, result)
        return result


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


def get_common_ancestor(type_1, type_2, context):
    object_type = context.get_type("Object")
    if type_1 == object_type or type_2 == object_type:
        return object_type

    typex = type_1
    while typex is not None and typex != object_type:
        if type_2.conforms_to(typex):
            return typex
        typex = typex.parent

    typex = type_2
    while typex is not None and typex != object_type:
        if type_1.conforms_to(typex):
            return typex
        typex = typex.parent

    return object_type

