import time
import numpy as np
import os
import networkx as nx
from collections import deque
from random import randrange
from tqdm import tqdm
import gzip
from scipy.stats import variation, entropy
import statistics
import urllib.request
import contextlib
import ssl

from utils import getGreedyCliques, greedyClique, parseDimacGraph, getXEntry, getYEntry, parseGraph

X_d = []
y_d = []


stem = 'Data/dimacs/'#'https://mat.gsia.cmu.edu/COLOR04/INSTANCES/'
dimacs = open('Data/dimacs_list.txt', )
#context = ssl._create_unverified_context()

for dimac in tqdm(dimacs):
    #print(dimac)
    dimac = dimac.strip()
    G = parseGraph(stem + dimac)
    #with contextlib.closing(urllib.request.urlopen(stem + dimac, context = context)) as u:
        #G = parseDimacGraph(u)
    X_d.append(getXEntry(G))
    #y_d.append(getYEntry(G))
dimacs.close()

write_X = open('Data/clique_measurements/dimacs_X', 'w')
#write_y = open('./dimacs_y', 'w')

for x in X_d:
    write_X.write(str(x) + '\n')

#for i in y_d:
   # write_y.write(str(i) + '\n')

write_X.close()
#write_y.close()