from phply import phpast, phpparse, phplex
import networkx as nx
import pprint
from definition.ast_node import ASTNode
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout
from networkx.drawing.nx_pydot import to_pydot


def parse_php_file(filename):
    """
    Parese a PHP file and return the AST.

    :param filename: The path to the PHP file.
    """
    with open(filename, 'r') as f:
        code = f.read()
    lexer = phplex.lexer.clone()
    parser = phpparse.make_parser()
    parsed = parser.parse(code, lexer=lexer)
    return parsed


def construct_cfg(cfg, node, parent=None):
    """
    Process nodes with different types and add them to the CFG if necessary.

    :param cfg: The control flow graph.
    :param node: The current node.
    :param parent: The parent of the current node.
    """
    node_printer(node)
    cfs = ["If", "ElseIf", "Else", "While", "DoWhile", "For",
           "Foreach", "ForeachVariable", "Switch", "Case", "Default"]
    node_type = node.__class__.__name__

    # Add control flow statements to the CFG
    if node_type in cfs:
        # Build and add the node to the CFG
        node_value = node.expr if hasattr(node, 'expr') else None
        current_node = ASTNode(
            node_type, node_value=node_value, node_lineno=node.lineno)
        cfg.add_edge(parent, current_node)

        # Regular cases as long as the node has a node/nodes attribute
        if hasattr(node, 'node') and node.node is not None:
            construct_cfg(cfg, node.node, parent=current_node)
        elif hasattr(node, 'nodes') and node.nodes is not None:
            for n in node.nodes:
                construct_cfg(cfg, n, parent=current_node)

        # Special case for If statements
        if node_type == "If":
            for ei in node.elseifs:
                construct_cfg(cfg, ei, parent=current_node)
            construct_cfg(cfg, node.else_, parent=current_node)

    # Special case for Block
    elif node_type == "Block":
        # If there is a child that is a control flow statement
        for n in node.nodes:
            if n.__class__.__name__ in cfs:
                # The parent of the child is the current node's parent
                construct_cfg(cfg, n, parent=parent)

    # Special case for Function
    elif node_type == "Function":
        # Build and add the node to the CFG
        node_value = node.name if hasattr(node, 'name') else None
        current_node = ASTNode(
            node_type, node_value=node_value, node_lineno=node.lineno)
        cfg.add_node(current_node)

        # The function node is the parent of its callee
        for n in node.nodes:
            if n.__class__.__name__ in cfs + ["FunctionCall", "MethodCall"]:
                # The parent of the child is the current node's parent
                construct_cfg(cfg, n, parent=current_node)

    # Special case for FunctionCall
    elif node_type == "FunctionCall":
        # Build and add the node to the CFG
        current_node = ASTNode(node_type, node_lineno=node.lineno)
        cfg.add_edge(parent, current_node)

        # Find the callee node and add an edge to it
        for n in cfg.nodes:
            if n.node_value == node.name:
                callee_node = n
                break
        cfg.add_edge(current_node, callee_node)

    # Special case for Class
    elif node_type == "Class":
        # Build and add the node to the CFG
        node_value = node.name if hasattr(node, 'name') else None
        current_node = ASTNode(
            node_type, node_value=node_value, node_lineno=node.lineno)
        cfg.add_node(current_node)

        # The class node is the parent of its method
        for n in node.nodes:
            if n.__class__.__name__ in cfs + ["FunctionCall", "MethodCall", "Method"]:
                # The parent of the child is the current node
                construct_cfg(cfg, n, parent=current_node)

    # Special case for Method
    elif node_type == "Method":
        # Build and add the node to the CFG
        node_value = node.name if hasattr(node, 'name') else None
        current_node = ASTNode(
            node_type, node_value=node_value, node_lineno=node.lineno)
        cfg.add_edge(parent, current_node)

        # The function node is the parent of its callee
        for n in node.nodes:
            if n.__class__.__name__ in cfs + ["FunctionCall", "MethodCall"]:
                # The parent of the child is the current node's parent
                construct_cfg(cfg, n, parent=current_node)

    # Special case for MethodCall or StaticMethodCall
    elif node_type == "MethodCall" or node_type == "StaticMethodCall":
        # Build and add the node to the CFG
        current_node = ASTNode(node_type, node_lineno=node.lineno)
        cfg.add_edge(parent, current_node)
        # Find the callee node and add an edge to it
        for n in cfg.nodes:
            if n.node_value == node.name:
                callee_node = n
                break
        cfg.add_edge(current_node, callee_node)


def node_printer(node):
    """
    A test function to print the node.

    :param node: The node to be printed.
    """
    for i in node.fields:
        print(i, '\t', node.__getattribute__(i))
    print('-----------------')


if __name__ == '__main__':
    # Initialize the CFG and add the start node
    cfg = nx.DiGraph()
    start_node = ASTNode("Start", node_lineno=0)

    # Parse the PHP file and construct the CFG
    parsed = parse_php_file('test/class.php')
    print(len(parsed))
    for node in parsed:
        construct_cfg(cfg, node, parent=start_node)

    # Draw the CFG
    print(cfg)
    labels = {node: ": ".join([node.node_type, str(node.node_lineno)])
              for node in cfg.nodes}
    color_map = {
        "If": "red",
        "ElseIf": "orange",
        "Else": "yellow",
        "While": "green",
        "DoWhile": "lime",
        "For": "blue",
        "Foreach": "purple",
        "ForeachVariable": "pink",
        "Switch": "brown",
        "Case": "gray",
        "Default": "black",
        "Function": "cyan",
        "FunctionCall": "magenta",
        "Start": "white",
        "Class": "olive",
        "Method": "teal",
        "MethodCall": "coral",
    }
    pos = nx.arf_layout(cfg)
    fig = plt.figure(figsize=(10, 10))
    nx.draw(cfg, pos=pos, with_labels=True, labels=labels, node_color=[
            color_map.get(node.node_type, "blue") for node in cfg.nodes])
    plt.show()
