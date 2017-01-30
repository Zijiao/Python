"""
GRAPH = {0: set([1, 2, 4]),
          1: set([0]),
          2: set([0]),
          3: set([]),
          4: set([0]),
          5: set([6, 7]),
          6: set([5]),
          7: set([5])}
"""


def bfs_visited(ugraph, start_node):
    """
    Breadth First Search
    """
    queue = []
    visited = set([start_node])
    queue.append(start_node)
    
    while len(queue) != 0:
        current_node = queue.pop(0)
        for node in ugraph[current_node]:
            if node not in visited:
                visited.add(node)
                queue.append(node)

    return visited

def cc_visited(ugraph):
    """
    Connected Components
    """
    remain_nodes = set([]) 
    for node in ugraph:
        remain_nodes.add(node)
    connected_comp = []
    
    while len(remain_nodes) != 0:
        current_node = remain_nodes.pop()
        current_comp = bfs_visited(ugraph, current_node)
        connected_comp.append(current_comp)
        remain_nodes = remain_nodes.difference(current_comp)
        
    return connected_comp
        
def largest_cc_size(ugraph):
    """
    Largest size of among all connected components
    """
    connected_comp = cc_visited(ugraph)
    largest_size = 0
    for elem in connected_comp:
        if len(elem) > largest_size:
            largest_size = len(elem)
    return largest_size

def compute_resilience(ugraph, attack_order):
    """
    return a list of resilience
    """
    resilience_list = [largest_cc_size(ugraph)]
    for attack_node in attack_order:
        del ugraph[attack_node]
        for node in ugraph:
               if attack_node in ugraph[node]:
                   ugraph[node].remove(attack_node)
        
        resilience_list.append(largest_cc_size(ugraph))
    
    return resilience_list