import subprocess
import os
import re

from antcol import Ant, solve
from tqdm import tqdm
#from  import *
import networkx as nx

#from my_ils import *
#from my_tabu import *

import copy
import random
import os
import time
from igraph import *
import igraph
import gc

from utils import parseGraph

CPN_IDX = 0
NPC_IDX = 1

#def make_friendly(g: nx.Graph):

y = []
# chi1000
datasets = ['dimacs']#, 'chi1000', 'chi500', 'dimacs', 'testset']
for curr_dataset in datasets:
    stem = 'Data/' + curr_dataset
    graphsToUse = []
    graphFile = open(str(stem + '_list.txt'))
    for line in graphFile:
        graphsToUse.append(line.strip())
    graphFile.close()

    for graph in tqdm(graphsToUse):
        #g = parseGraph(stem + '/' + graph)
        g = nx.erdos_renyi_graph(100, .5)
        # Gotta make sure graph is fucking friendly, I guess, wow
        #g = ig.to_networkx()

        start = max(nx.greedy_color(g, 'DSATUR').values())
        initial = time.process_time()
        num_colors, _, _ = solve(g)
        time_taken = time.process_time() - initial
        print(start, num_colors, time_taken)
        y.append((start, num_colors, time_taken))
"""
write_y = open(str('Empirical Data/ant_col_res' + curr_dataset + '_y'), 'w')
write_y.write('DSATUR, TABU, TIME\n')

for i in tqdm(y):
    write_y.write(str(i) + '\n')
write_y.close()
"""