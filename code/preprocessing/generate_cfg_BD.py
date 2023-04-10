from phply import phpast, phpparse, phplex
import networkx as nx
import pprint
from definition.ast_node import ASTNode
import matplotlib.pyplot as plt
from collections import deque
import random
import argparse
import os
from time import sleep
import csv
import json


def parse_php_file(file_path):
    '''
    Parese a PHP file and return the AST.

    :param file_path: The absulate path to the PHP file.
    '''
    with open(file_path, 'r') as f:
        code = f.read()
    lexer = phplex.lexer.clone()
    parser = phpparse.make_parser()
    parsed = parser.parse(code, lexer=lexer)
    return parsed


def construct_cfg(cfg, node, parent=None, file_path=None):
    '''
    Process nodes with different types and add them to the CFG if necessary.

    :param cfg: The control flow graph.
    :param node: The current node.
    :param parent: The parent of the current node.
    :param file_path: The absulate path of the current node.
    '''
    # node_printer(node)
    cfs = ['If', 'ElseIf', 'Else', 'While', 'DoWhile', 'For',
           'Foreach', 'Switch', 'Case', 'Default', 'InlineHTML']
    node_type = node.__class__.__name__

    # Add control flow statements to the CFG (InlineHTML to avoid nosence accessable code blocks)
    if node_type in cfs:
        # Build and add the node to the CFG
        node_value = node.expr if hasattr(node, 'expr') else None
        current_node = ASTNode(
            node_type, node_value=node_value, node_lineno=node.lineno, node_file=file_path)
        cfg.add_edge(parent, current_node)

        # Regular cases as long as the node has a node/nodes attribute
        if hasattr(node, 'node') and node.node is not None:
            construct_cfg(cfg, node.node, parent=current_node,
                          file_path=file_path)
        elif hasattr(node, 'nodes') and node.nodes is not None:
            for n in node.nodes:
                construct_cfg(cfg, n, parent=current_node, file_path=file_path)

        # Special case for If statements
        if node_type == 'If':
            for ei in node.elseifs:
                construct_cfg(cfg, ei, parent=current_node,
                              file_path=file_path)
            if node.else_ is not None:
                construct_cfg(cfg, node.else_,
                              parent=current_node, file_path=file_path)

    # Special case for Block
    elif node_type == 'Block':
        # If there is a child that is a control flow statement
        for n in node.nodes:
            # The parent of the child is the current node's parent
            construct_cfg(cfg, n, parent=parent, file_path=file_path)

    # Special case for Function
    elif node_type == 'Function':
        # Build and add the node to the CFG
        node_value = node.name if hasattr(node, 'name') else None
        current_node = ASTNode(
            node_type, node_value=node_value, node_lineno=node.lineno, node_file=file_path)
        cfg.add_node(current_node)

        # The function node is the parent of its callee
        for n in node.nodes:
            if n.__class__.__name__ in cfs + ['FunctionCall', 'MethodCall']:
                # The parent of the child is the current node's parent
                construct_cfg(cfg, n, parent=current_node, file_path=file_path)

    # Special case for FunctionCall
    elif node_type == 'FunctionCall':
        # Build and add the node to the CFG
        current_node = ASTNode(
            node_type, node_lineno=node.lineno, node_file=file_path)
        cfg.add_edge(parent, current_node)
        callee_node = None
        # Find the callee node and add an edge to it
        possible_childs = [n for n in cfg.nodes if n.node_value == node.name]
        if possible_childs == []:
            callee_node = ASTNode(
                'Not_Exist_' + node.name, node_value=node.name, node_lineno=node.lineno, node_file=file_path)
        else:
            for pc in possible_childs:
                cfg.add_edge(current_node, pc)

    # Special case for Class
    elif node_type == 'Class':
        # Build and add the node to the CFG
        node_value = node.name if hasattr(node, 'name') else None
        current_node = ASTNode(
            node_type, node_value=node_value, node_lineno=node.lineno, node_file=file_path)
        cfg.add_node(current_node)

        # The class node is the parent of its method
        for n in node.nodes:
            if n.__class__.__name__ in cfs + ['FunctionCall', 'MethodCall', 'Method']:
                # The parent of the child is the current node
                construct_cfg(cfg, n, parent=current_node, file_path=file_path)

    # Special case for Method
    elif node_type == 'Method':
        # Build and add the node to the CFG
        node_value = node.name if hasattr(node, 'name') else None
        current_node = ASTNode(
            node_type, node_value=node_value, node_lineno=node.lineno, node_file=file_path)
        cfg.add_edge(parent, current_node)

        # The function node is the parent of its callee
        for n in node.nodes:
            if n.__class__.__name__ in cfs + ['FunctionCall', 'MethodCall']:
                # The parent of the child is the current node's parent
                construct_cfg(cfg, n, parent=current_node, file_path=file_path)

    # Special case for MethodCall or StaticMethodCall
    elif node_type == 'MethodCall' or node_type == 'StaticMethodCall':
        # Build and add the node to the CFG
        current_node = ASTNode(
            node_type, node_lineno=node.lineno, node_file=file_path)
        cfg.add_edge(parent, current_node)
        callee_node = None
        # Find the callee node and add an edge to it
        possible_childs = [n for n in cfg.nodes if n.node_value == node.name]
        if possible_childs == []:
            callee_node = ASTNode(
                'Not_Exist_' + node.name, node_value=node.name, node_lineno=node.lineno, node_file=file_path)
        else:
            for pc in possible_childs:
                cfg.add_edge(current_node, pc)
                
    # Special case for File Include/Require
    elif node_type in ['Include', 'Require']:
        for suspecious_node in cfg.nodes:
            if suspecious_node.node_value == node.expr and suspecious_node.node_type in ['Include', 'Require']:
            # The included file is already in the CFG
            # Find the nodes linked with piror Include_Node and add edges to them
                current_node = ASTNode(
                node_type, node_value=node.expr, node_lineno=node.lineno, node_file=file_path)
                cfg.add_edge(parent, current_node)
                out_edges = cfg.out_edges(suspecious_node)
                for piror_include_node, child in out_edges:
                    cfg.add_edge(current_node, child)
                return
        # The included file is not in the CFG
        # Build and add the node to the CFG, also process the included file
        current_node = ASTNode(
            node_type, node_value=node.expr, node_lineno=node.lineno, node_file=file_path)
        cfg.add_edge(parent, current_node)
        file_path_list = file_path.split('/')
        real_file_path = '/'.join(file_path_list[:-1]) + '/' + node.expr
        parsed = parse_php_file(real_file_path)
        for n in parsed:
            # The file of each n is the included file
            construct_cfg(cfg, n, parent=current_node,
                            file_path=real_file_path)

    # Special case for UseDeclarations TODO: Not finished yet, but should we process use statements? Is it necessary?
    # elif node_type == 'UseDeclarations':
    #     # Process each use declaration
    #     for n in node.nodes:
    #         # The type of each n in nodes node is UseDeclaration

    #         names = n.name.split('\\')
    #         parsed = parse_php_file(names[0])

    #         # Compare the name of each node in the parsed file with the last name in the use declaration
    #         for p in parsed:
    #             if p.hasattr('name') and p.name == names[-1]:
    #                 current_node = ASTNode('UseDeclaration', node_value=n.alias, node_lineno=n.lineno, node_file=file_path)
    #                 cfg.add_edge(current_node, p)
    #                 construct_cfg(cfg, p, parent=current_node, file_path=names[0])
    #                 break
    #             i += 1


# Calculate the distance of each node from the target node using BFS
def calculate_distances(cfg):
    target_node = None
    for node in cfg.nodes():
        if node.is_target:
            target_node = node
            break
    
    distances = {node: float('inf') for node in cfg.nodes()}
    distances[target_node] = 0

    queue = deque([target_node])
    visited = set()

    while queue:
        current_node = queue.popleft()
        visited.add(current_node)
        for neighbor in cfg.predecessors(current_node):
            if neighbor not in visited:
                distances[neighbor] = min(
                    distances[neighbor], distances[current_node] + 1)
                queue.append(neighbor)

    for node, distance in distances.items():
        node.node_distance = distance


def node_printer(node):
    '''
    A test function to print the node.

    :param node: The node to be printed.
    '''
    print(node)
    for i in node.fields:
        print(i, '\t', node.__getattribute__(i))
    print('-----------------')


def save_to_csv(nodes, file_name):
    '''
    Save the nodes to a CSV file.

    :param nodes: The nodes.
    :param file_name: The name of the CSV file.
    '''

    with open('info/distance/' + file_name + '.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['node_file', 'node_lineno',
                        'node_type', 'node_distance'])
        for node in nodes:
            writer.writerow([node.node_file, node.node_lineno, node.node_type, node.node_distance])
            
def save_to_json(nodes, file_name):
    '''
    Save the nodes to a JSON file.

    :param nodes: The nodes.
    :param file_name: The name of the JSON file.
    '''
    data = {'nodes': []}
    for node in nodes:
        data['nodes'].append({
            'node_file': node.node_file,
            'node_lineno': node.node_lineno,
            'node_type': node.node_type,
            'node_distance': node.node_distance
        })
    with open('info/distance/' + file_name + '.json', 'w') as jsonfile:
        json.dump(data, jsonfile, indent=4)


if __name__ == '__main__':
    # set a parser to process the arguments from the command line
    parser = argparse.ArgumentParser()
    parser.add_argument('-E', '--entry', type=str,
                        required=False, help="Path to the entry file")
    parser.add_argument('-T', '--target', type=str, required=False,
                        help="The string of the target function (format: path:line_number, e.g., ./file3.php:8)")

    entry_path = parser.parse_args().entry
    target = parser.parse_args().target

    # Initialize the CFG and add the start node
    cfg = nx.DiGraph()
    start_node = ASTNode('Start', node_lineno=0, node_file='Start')

    # Default args for test and debug
    if entry_path is None:
        entry_path = '/var/www/html/index.php'
    if target is None:
        target = '/var/www/html/file4.php:22'

    # Get the absolute path of the entry function and the target
    entry_path = os.path.abspath(entry_path)
    target = os.path.abspath(target.split(':')[0]) + ':' + target.split(':')[1]

    # Parse the PHP file and construct the CFG
    parsed = parse_php_file(entry_path)
    for node in parsed:
        construct_cfg(cfg, node, parent=start_node, file_path=entry_path)

    # Add the target node to the CFG
    target_node = None
    closest_node = None
    smallest_distance = float('inf')
    target_file, target_lineno = target.split(':')
    for node in cfg.nodes():
        if node.node_file == target_file:
            interval = int(target_lineno) - node.node_lineno
            if interval == 0:
                target_node = node
                break
            elif interval > 0 and interval < smallest_distance:
                closest_node = node
                smallest_distance = interval
    if target_node is None:
        target_node = closest_node
        
    try:
        target_node.is_target = True
    except:
        raise Exception('Target node not found! Please check the target path and line number.')

    # Calculate distances from target node to each node
    calculate_distances(cfg)

    # Draw the CFG
    print(cfg)
    labels = {node: ':'.join([str(node.node_file), str(node.node_lineno), node.node_type, str(node.node_distance)])
              for node in cfg.nodes}
    color_map = {
        'If': 'red',
        'ElseIf': 'orange',
        'Else': 'yellow',
        'While': 'green',
        'DoWhile': 'lime',
        'For': 'blue',
        'Foreach': 'purple',
        'Switch': 'brown',
        'Case': 'gray',
        'Default': 'black',
        'Function': 'cyan',
        'FunctionCall': 'magenta',
        'Start': 'pink',
        'Class': 'olive',
        'Method': 'teal',
        'MethodCall': 'coral',
        'StaticMethodCall': 'gold',
        'Include': 'silver',
        'Require': 'silver'
    }
    pos = nx.arf_layout(cfg)
    fig = plt.figure(figsize=(10, 10))
    nx.draw(cfg, pos=pos, with_labels=True, labels=labels, node_color=[
            color_map.get(node.node_type, 'blue') for node in cfg.nodes], font_size=8)
    plt.show()

    # Write the CFG to a graphml file for further processing
    nx.write_graphml(cfg, r'info/graphml/' +
                     entry_path.split(r'/')[-1] + '.graphml')
    # Write the nodes to a CSV file for further processing
    save_to_json(cfg.nodes(), entry_path.split(r'/')[-1])
