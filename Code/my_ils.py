import networkx as nx
import random
from collections import defaultdict

from collections import defaultdict, deque
import itertools

import networkx as nx
from networkx.utils import arbitrary_element
from networkx.utils import py_random_state

from my_tabu import tabu
from utils import *
#from tabucol import tabucol
import copy

# Coloring
CPN_IDX = 0
NPC_IDX = 1

# Taken from networkx, colors in place
def dsat(G, colors, op_count):
    distinct_colors = {v: set() for v in G}
    for i in range(len(G)):
        # On the first time through, simply choose the node of highest degree.
        if i == 0:
            node = max(G, key=G.degree)
            yield node
            # Add the color 0 to the distinct colors set for each
            # neighbors of that node.
            for v in G[node]:
                op_count[0] += 1
                distinct_colors[v].add(0)
        else:
            # Compute the maximum saturation and the set of nodes that
            # achieve that saturation.
            saturation = {
                v: len(c) for v, c in distinct_colors.items() if v not in colors
            }
            # Yield the node with the highest saturation, and break ties by
            # degree.
            node = max(saturation, key=lambda v: (saturation[v], G.degree(v)))
            yield node
            # Update the distinct color sets for the neighbors.
            color = colors[node]
            for v in G[node]:
                op_count[0] += 1
                distinct_colors[v].add(color)

def get_satur(g: nx.Graph, coloring: (dict, dict), v: int, op_count: list) -> int:
    colors = set()
    for u in g[v]:
        op_count[0] += 1
        colors.add(coloring[CPN_IDX][u])
    return len(colors)

def perturb_with_given(g: nx.Graph, coloring: (dict, dict), op_count: list) -> None:
    gamma = .05
    colors_to_remove = (random.sample(
        range(len(coloring[NPC_IDX])), 
        int(gamma * len(coloring[NPC_IDX]))
    ))

    nodes_to_recolor = set()
    for r in colors_to_remove:
        nodes = coloring[NPC_IDX].pop(r)
        for n in nodes:
            op_count[0] += 1
            coloring[CPN_IDX].pop(n)
        nodes_to_recolor.update(nodes)
        #nodes_to_recolor += [(get_satur(g, coloring, v), len(g[v]), v) for v in nodes]
    nodes = dsat(g, coloring[CPN_IDX], op_count)
    for n in nodes:

        if n not in nodes_to_recolor: 
            continue
        
        neighbour_colors = {coloring[CPN_IDX][v] for v in g[n] if v in coloring[CPN_IDX]}
        for color in range(coloring[NPC_IDX]):
            op_count[0] += 1
            if color not in neighbour_colors:
                break
        coloring[NPC_IDX][color].add(n)
        coloring[CPN_IDX][n] = color

        nodes_to_recolor.discard(n)
        if len(nodes_to_recolor) == 0:
            break


    # Now, we need to update NPC
    #for node, color in coloring[CPN_IDX].items():
    #    coloring[NPC_IDX][color].add(node)
    
    # And we're done

# perturbs in place
# Alternitively, we don't even have to use this one, we can just use the nx dsatur algorithm.
def perturb(g: nx.Graph, coloring: (dict, dict), op_count: list) -> None:

    # Remove a set number of colors (based on gamma from An application of ILS to GCP) gamma = .05
    gamma = .05
    colors_to_remove = (random.sample(
        range(len(coloring[NPC_IDX])), 
        int(gamma * len(coloring[NPC_IDX]))
    ))

    nodes_to_recolor = []
    for r in colors_to_remove:
        op_count[0] += 1
        nodes = coloring[NPC_IDX].pop(r)
        nodes_to_recolor += [(get_satur(g, coloring, v, op_count), len(g[v]), v) for v in nodes]
    
    nodes_to_recolor.sort(reverse=True)
    for _, _, n in nodes_to_recolor:
        # Color this node with the lowest possible color
        try_color = 0

        # Make sure no infinite loop
        while True:
            if set(nx.neighbors(g, n)).intersection(coloring[NPC_IDX][try_color]) == 0:
                # Recolor
                coloring[NPC_IDX][try_color].add(n)
                coloring[CPN_IDX][n] = try_color
                
                break
            try_color += 1
            op_count[0] += 1          

def ils(g: nx.Graph, op_count: list) -> dict:
    # Generate initial solution with DSATUR

    #coloring = (dict(), defaultdict(set))
    #dsatur(g, coloring[CPN_IDX]) I guess this is bust for now...
    coloring = (nx.greedy_color(g, strategy='DSATUR'), defaultdict(set))
    # Now, we need to update NPC
    for node, color in coloring[CPN_IDX].items():
        coloring[NPC_IDX][color].add(node)

    # Do initial local search with tabu
    while True:
        
        new_coloring = copy.deepcopy(coloring)
        # Pertub current solution with DSAT (as per an applicaiton of ILS to GCP)
        #perturb_with_given(g, new_coloring, op_count)
        perturb(g, new_coloring, op_count)

        # Local search with tabu (We can actually do this with multiple iterations)
        new_coloring = tabu(g, new_coloring[CPN_IDX], new_coloring[NPC_IDX], 200, op_count)

        # Compare coloring (I think the paper says to accept every new coloring)
        if len(new_coloring[NPC_IDX]) < len(coloring[NPC_IDX]):
            coloring = new_coloring
        else:
            break

        op_count[0] += 1
    return coloring[CPN_IDX]

def test1(g):
    print(max(ils(g).values()))

#g = parseGraph('Data\chi500\G-500-0.1--.3.col')
#test1(g)
#colors = {}
#print(dsat(nx.erdos_renyi_graph(100, .9, 1), colors))
#print(colors)
#print(max(nx.greedy_color(g, strategy='DSATUR').values()))