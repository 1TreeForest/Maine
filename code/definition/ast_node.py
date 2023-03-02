class ASTNode:
    """
    A class to represent an abstract syntax tree (AST) node.
    """

    def __init__(self, node_type, node_lineno = None, node_value=None, node_file = None):
        """
        Initialize an AST node.

        :param node_type: The type of the node (e.g., "Function").
        :param node_lineno: The lineno of the node (e.g., "1").
        :param node_value: The value of the node (e.g., the name of the function).
        :param node_file: The filename of the node.
        """
        self.node_type = node_type
        self.node_lineno = node_lineno
        self.node_value = node_value
        self.node_file = node_file

    # def add_child(self, child_node):
    #     """
    #     Add a child node to the current node.

    #     :param child_node: The child node to add.
    #     """
    #     self.children.append(child_node)