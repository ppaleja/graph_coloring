import subprocess
import os
import re

from tqdm import tqdm
#from  import *
import networkx as nx
#from my_ils import *
#from my_tabu import *

import copy
import random
import os

CPN_IDX = 0
NPC_IDX = 1

datasets = ['dimacs', 'chi1000', 'chi500', 'dimacs', 'testset']
for curr_dataset in datasets:
    stem = '../Data/' + curr_dataset
    graphsToUse = []
    graphFile = open(str(stem + '_list.txt'))
    for line in graphFile:
        graphsToUse.append(line.strip())
    graphFile.close()

    for graph in tqdm(graphsToUse):
        