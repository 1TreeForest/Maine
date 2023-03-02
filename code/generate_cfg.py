from phply import phpast, phpparse, phplex
import networkx as nx
import pprint
from definition.ast_node import ASTNode
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout
from networkx.drawing.nx_pydot import to_pydot

# Parse a PHP file
def parse_php_file(filename):
    # Parse the PHP file
    with open(filename, 'r') as f:
        code = f.read()
    lexer = phplex.lexer.clone()
    parser = phpparse.make_parser()
    parsed = parser.parse(code, lexer=lexer)
    # phpast.resolve_magic_constants(parsed)
    # pprint.pprint(parsed)
    return parsed

# Add edges to the CFG
def construct_cfg(cfg, node, parent=None):
    global node_lineno
    # Only add edges for control flow statements
    cfs = ["If", "ElseIf", "Else", "While", "DoWhile", "For",
           "Foreach", "ForeachVariable", "Switch", "Case", "Default"]
    node_type = node.__class__.__name__
    if node_type in cfs:
        # Build and add the node to the CFG
        node_value = node.expr if hasattr(node, 'expr') else None
        current_node = ASTNode(node_type, node_value=node_value, node_lineno=node.lineno)
        cfg.add_edge(parent, current_node, label=node_type)

        # Regular cases as long as the node has a node/nodes attribute
        if hasattr(node, 'node') and node.node is not None:
            construct_cfg(cfg, node.node, parent=current_node)
        if hasattr(node, 'nodes') and node.nodes is not None:
            for n in node.nodes:
                construct_cfg(cfg, n, parent=current_node)

        # Special case for If statements
        if node_type == "If":
            for ei in node.elseifs:
                construct_cfg(cfg, ei, parent=current_node)
            construct_cfg(cfg, node.else_, parent=current_node)
        for i in node.fields:
            print(i, '\t', node.__getattribute__(i))
                    # Special case for For statements
                    # if node_type == "For":
                    #     if node.elseifs is not None:
                    #         for ei in node.elseifs:
                    #             construct_cfg(cfg, ei, parent=current_node)
                    #     if node.else_ is not None:
                    #         construct_cfg(cfg, node.else_, parent=current_node)

                    # # Special case for Foreach statements
                    # if node_type == "Foreach":
                    #     if node.elseifs is not None:
                    #         for ei in node.elseifs:
                    #             construct_cfg(cfg, ei, parent=current_node)
                    #     if node.else_ is not None:
                    #         construct_cfg(cfg, node.else_, parent=current_node)
    # Special case for Block statements
    elif node_type == "Block":
        # If there is a child that is a control flow statement
        for n in node.nodes:
            if n.__class__.__name__ in cfs:
                # The parent of the child is the current node's parent
                construct_cfg(cfg, n, parent=parent)


if __name__ == '__main__':
    # Initialize the CFG and add the start node
    cfg = nx.DiGraph()
    start_node = ASTNode("Start", node_lineno=0)

    # Parse the PHP file and construct the CFG
    parsed = parse_php_file('test/foreach.php')
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
        "Default": "black"
    }
    pos = nx.shell_layout(cfg)
    nx.draw(cfg, with_labels=True, labels=labels, node_color=[
            color_map.get(node.node_type, "blue") for node in cfg.nodes])
    plt.show()
