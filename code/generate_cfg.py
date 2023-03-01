from phply import phpast, phpparse, phplex
import networkx as nx

# Define a function to generate a control flow graph
def generate_cfg(filename):
    # Parse the PHP file
    with open(filename, 'r') as f:
        code = f.read()
    lexer = phplex.lexer.clone()
    parser = phpparse.make_parser()
    parsed = parser.parse(code, lexer=lexer)
    # Create a directed graph to represent the CFG
    cfg = nx.DiGraph()
    
    # Traverse the parsed AST and add edges to the CFG
    add_edges(parsed, cfg) #TODO above is success, but this line and below have errors.

    return cfg

# Define a helper function to add edges to the CFG
def add_edges(nodes, cfg, parent=None):
    for node in nodes:
        if parent is not None:
            cfg.add_edge(parent, node)
        if isinstance(node, phpast.If):
            # Add edges for the if statement's condition and body
            cfg.add_edge(node, node)
            add_edges(node.body, node)
            # Add edges for the else statement's body (if it exists)
            if node.else_:
                add_edges(node.else_, node)
        elif isinstance(node, phpast.While):
            # Add edges for the while loop's condition and body
            cfg.add_edge(node, node.test)
            add_edges(node.body, node)
        elif isinstance(node, phpast.DoWhile):
            # Add edges for the do-while loop's body and condition
            add_edges(node.body, node)
            cfg.add_edge(node, node.test)
        elif isinstance(node, phpast.For):
            # Add edges for the for loop's init, condition, and increment,
            # as well as its body
            if node.init:
                add_edges(node.init, node)
            if node.test:
                cfg.add_edge(node, node.test)
                add_edges(node.test, node)
            if node.increment:
                add_edges(node.increment, node)
            add_edges(node.body, node)
        elif isinstance(node, phpast.Foreach):
            # Add edges for the foreach loop's iterable and body
            cfg.add_edge(node, node.expr)
            add_edges(node.body, node)
        elif isinstance(node, phpast.Switch):
            # Add edges for the switch statement's condition and cases
            cfg.add_edge(node, node.test)
            for case in node.cases:
                add_edges(case, node)

if __name__ == '__main__':
    print(generate_cfg("test/test.php"))