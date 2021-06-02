import networkx as nx
import copy
import random
import math

from tqdm import tqdm

from collections import defaultdict, OrderedDict

import utils

TQDM = False

"""
Basically, we have to now get a 'coloring' that is exactly the target.
It can be wrong, we will improve it:
 
Methodology (from paper): Given a coloring with k colors, recolor the kth color 
with a color that minimizes conflicts
"""

# Why do we need target??, I don't think we actually do
def regenerate(g: nx.Graph, color_per_node: dict, nodes_per_color: dict, target: int, op_count: list) -> None:

    # We should give more randomness by making the color to remove random, I think....

    color_to_remove: int = max(nodes_per_color.keys())
    # Ok, so there's a bunch of empty colorings? WTF
    if color_to_remove == 0: return
    for v in (tqdm(nodes_per_color.pop(color_to_remove), 'In regenerate: ') if TQDM else 
        nodes_per_color.pop(color_to_remove)):
        best = (float('inf') , None)
        for color, nodes in nodes_per_color.items():
            num_conflicts = 0
            for check in nodes:
                op_count[0] += 1
                # Check if the number of conflicts
                num_conflicts += int(check in g[v])
            if best[0] > num_conflicts:
                best = (num_conflicts, color)
        # Recolor v with the best one
        color_per_node[v] = best[1]
        nodes_per_color[best[1]].add(v)
    
    assert color_to_remove not in nodes_per_color
    # I think what we should return is the number of conflicts per node....

# Gets number of conflicts # Takes O(|E|) time (seems to be the bottleneck)
def obj_func(g: nx.Graph, color_per_node: dict, nodes_per_color: dict, op_count: list) -> list:
    # We want to count the number of times that the node gets colored the same as its neighbors
    #for color, nodes in nodes_per_color:
    conflicts = list()
    # Just loop over all the edges in g and add 1 if they have the same color (technically its conflicts * 2 but)
    for e in (g.edges if not TQDM else tqdm(g.edges, 'In obj_func: ')):
        # Instead, let's literally return the conflicts indices
        op_count[0] += 1
        if color_per_node[e[0]] == color_per_node[e[1]]:
            conflicts.append(frozenset([e[0], e[1]]))
        #conflicts += bool(color_per_node[e[0]] == color_per_node[e[1]])
    return list(map(tuple, conflicts))

# Get's best neigbhor if t_n is 0, else get's the best tabu number
def best_neighbor(
    delta: defaultdict, 
    tabu_mat: defaultdict, 
    restriction: int, 
    color_per_node: dict,
    op_count: list
) -> ((int, int), int):

    # Just loop through each one and return arg_min?
    m = (None, float('inf')) # Should actually be 'net-conflicts'
    for neighbor, num_conflicts in (delta.items() if not TQDM else tqdm(delta.items(), 'Getting best neighbor')):
        op_count[0] += 1
        if (
            # Better solution
            num_conflicts < m[1] and

            # Not tabu, indexed by (node_changed, old_color) 
            tabu_mat.get((neighbor[0], color_per_node[neighbor[0]]), float('inf')) > restriction
        ):
            m = (neighbor, num_conflicts)
    return m #TODO: Ok, so the 'best' neighbor is getting set as something that doesn't exist......


    # So the neigbhorhood of a solution s is the set of 'single color' moves, where we only change
    # One color of one node, I think
    # So it's kind of like hamming distance of colors.

    # We make the neigbhorhood smaller by only removing conflicting nodes
    # Maybe in the above we have a boolean to denote conflicting colors?

    # |V| by k matrix used to store the effect of moving to each possible neighbor
# Tabu list base size is sqrt()

# Initialize the delta matrix that keeps track of how much we gain from a particular move
def init_delta(g: nx.Graph, nodes_per_color: dict, color_per_node: dict, conflicts: list, op_count: list) -> defaultdict:
    # We only have to make entries for colors that conflict
    d = defaultdict(int)
    # Check for conflicts by iterating through edges
    for n1, n2 in (conflicts if not TQDM else tqdm(conflicts, 'Initializing delta')):
        #print('help')
        # Add effect of changing color of node x to color j as stated in dimacs textbook pg 640
        for color in nodes_per_color.keys():
            # Count conflicts at this particular neigbhorhood. First n1, then n2?
            # n1
            for u in g[n1]:
                op_count[0] += 1
                # Great, I am skipping the current coloring
                if color == color_per_node[n1]: break
                
                d[(n1, color)] += int(color_per_node[u] == color) - int(color_per_node[u] == color_per_node[n1])
            
            for u in g[n2]:
                op_count[0] += 1
                if color == color_per_node[n2]: break
                
                d[(n2, color)] += int(color_per_node[u] == color) - int(color_per_node[u] == color_per_node[n2])
    return d
                
def update_sol(cpn: dict, npc: dict, node: int, new_color: int, op_count: list) -> None:
    npc[cpn[node]].discard(node) # Remove from original
    npc[new_color].add(node) # Add new color
    cpn[node] = new_color # Set the nodes color

def update_delta(
    g: nx.Graph, 
    delta: dict, 
    nodes_per_color: dict,
    color_per_node: dict,
    update_node: int, 
    update_color: int, 
    old_color: int,
    op_count: list
):

    # First, pop (up, uc) from delta
    delta.pop((update_node, update_color))

    # Wait, but also we have to update all the ones that update_node conflicted with as well

    # We need to keep track of the colors we've reset
    reset = set(nodes_per_color.keys())

    # Okay, so now, we have to get conflicts with 
    for u in (g[update_node] if not TQDM else tqdm(g[update_node], 'Updating delta: ')):

         # Decrement the ones that would have conflicted but now do not
        if (u, old_color) in delta:
            delta[(u, old_color)] -= 1

        # Increment the ones that now have another conflict because we changed currNode
        if (u, update_color) in delta:
            delta[(u, update_color)] += 1

        # So we need to update all the neighbor's with the old color and minus one to them (I think)
        for color in nodes_per_color.keys():
            op_count[0] += 1
            if color in reset:
                reset.discard(color)
                delta[update_node, color] = 0

            # Should I skip this current color???
            if color == update_color: continue

            delta[(update_node, color)] += (
                int(color_per_node[u] == color) - 
                int(color_per_node[u] == color_per_node[update_node])
            )

def tabu(g: nx.Graph, color_per_node: dict, nodes_per_color: dict, max_iter: int, op_count: list) -> (dict, dict):

    good_coloring = (copy.deepcopy(color_per_node), copy.deepcopy(nodes_per_color))

    # Initialize tabu matrix
    M = OrderedDict()

    # Initialize constants determined from "Tabu Search for graph coloring...."
    alpha = 2
    r = 10

    # Ok, so I don't think we need to do this regeneration step, any more....
    #target = int(max(nodes_per_color.keys()) * .95)
    target = len(nodes_per_color) - 1

    # Recolor in place (is this the best idea???)
    regenerate(g, color_per_node, nodes_per_color, target, op_count)

    # Now, we're going to do the iterations
    iter = 0
    while iter < max_iter:
        if iter % 50 == 0:
            print('Iter: {}, Target: {}'.format(iter, target))

        # Make a copy of current best curr_[blank] is the WORKING copy
        curr_CPN = copy.deepcopy(color_per_node) 
        curr_NPC = copy.deepcopy(nodes_per_color)

        orig_conflicts = obj_func(g, color_per_node, nodes_per_color, op_count)

        # Objective function???? So let's look back at the paper and see if we can compute this objective func
        # I feel like it would be the number of conflicts (f_p = len(conflicts))

        # TODO: Ok, so conflicts seems to still be operating under the previous colorings (still has colors)
        conflicts = copy.deepcopy(orig_conflicts)

        # Initialize delta matrix as stated on pg 8 of paper
        delta = init_delta(g, curr_NPC, curr_CPN, conflicts, op_count)
        #set_delta(delta, g, curr_CPN)

        while len(conflicts) > 0 and iter < max_iter:

            op_count[0] += 1

            if iter % 50 == 0:
                print('Iter: {}, Target: {}'.format(iter, target))
            # We need to get the 'best neighbor' of our current solution
            neighbor, neighbor_conflicts = best_neighbor(delta, M, 0, curr_CPN, op_count)
            old_color = curr_CPN[neighbor[0]]
            # If we got better, use it (aspiration criterion)
            # I think I actually need to do the objective function....
            temp_CPN = copy.deepcopy(curr_CPN)
            temp_NPC = copy.deepcopy(curr_NPC)
            update_sol(temp_CPN, temp_NPC, neighbor[0], neighbor[1], op_count)
            f_neighbor = obj_func(g, temp_CPN, temp_NPC, op_count)
            if len(f_neighbor) < len(conflicts):
                
                # change our current solution to this neighbor TODO: New colors are wrong somehow
                update_sol(curr_CPN, curr_NPC, neighbor[0], neighbor[1], op_count)
                # We actually also need to update delta here too

            else:
                # Get best non-tabu solution. What if there is no solution? 
                neighbor, neighbor_conflicts = best_neighbor(delta, M, iter, curr_CPN, op_count)
                if neighbor == None: break
                old_color = curr_CPN[neighbor[0]]
                update_sol(curr_CPN, curr_NPC, neighbor[0], neighbor[1], op_count)
                # And here
            
            # So update delta here
            update_delta(g, delta, curr_NPC, curr_CPN, neighbor[0], neighbor[1], old_color, op_count)

            # Need to make sure that tabu matrix isn't too long, size from DIMACS TB pg 240
            if len(M) > math.sqrt(2 * len(orig_conflicts) * max((nodes_per_color.keys()))):
                M.popitem(last=False)

            
            # Now we need to add an entry to the tabu matrix ()
            # l = alpha * |N(curr_solution)| / # target number of colors + random(1...g)
            l = alpha * int(len(delta) / target) + random.randrange(1, r)
            M[(neighbor[0], old_color)] = iter + l

            f_neighbor = obj_func(g, curr_CPN, curr_NPC, op_count)
            if len(f_neighbor) < len(conflicts):
                color_per_node = copy.deepcopy(curr_CPN)
                nodes_per_color = copy.deepcopy(curr_NPC)
                conflicts = copy.deepcopy(f_neighbor)
            
            iter += 1
        if len(obj_func(g, color_per_node, nodes_per_color, op_count)) == 0:
            good_coloring = (copy.deepcopy(color_per_node), copy.deepcopy(nodes_per_color))
            #target = int(max(nodes_per_color.keys()) * .95)
            target = len(nodes_per_color) - 1
            regenerate(g, color_per_node, nodes_per_color, target, op_count)
            iter = 0
            
            # If out tabu_sol gets a real solution then repeat the whole process
            # Do until we can't do any more then take the t-1 solution.

    return good_coloring

# Let's test it out, shall we
def test():
    #g = utils.parseGraph('../../Data/chi500/G-500-0.1--.1.col')
    g = nx.erdos_renyi_graph(500, .9, 1)
    #color_per_node = nx.greedy_color(g)
    # Let's try not giving a headstart, let's just try with a wrong coloring
    color_per_node = dict()
    for i, n in enumerate(g):
        color_per_node[n] = i
    color_per_node = nx.greedy_color(g)
    nodes_per_color = defaultdict(set)
    for n, c in color_per_node.items():
        nodes_per_color[c].add(n)


    op_count = [0]
    tabu(g, color_per_node, nodes_per_color, 200, op_count)
#test()
#tabu(parseGraph('../../Data/chi500/G-500-0.1--.1.col'), 200, True)
