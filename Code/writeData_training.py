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

from utils import getGreedyCliques, greedyClique, parseGraph, parseDimacGraph, getXEntry, getYEntry

X = []
y = []

# chi1000
graphsToUse = []
graphFile = open('../Data/chi1000_list.txt')
for line in graphFile:
    graphsToUse.append(line.strip())
graphFile.close()

stem = "../Data/chi1000/"
for graph in tqdm(graphsToUse):
    G = parseGraph(stem + graph)
    X.append(getXEntry(G))
    y.append(getYEntry(G))

# chi500
graphsToUse = []
graphFile = open('../Data/chi500_list.txt')
for line in graphFile:
    graphsToUse.append(line.strip())
graphFile.close()

stem = "../Data/chi500/"
for graph in tqdm(graphsToUse):
    G = parseGraph(stem + graph)
    X.append(getXEntry(G))
    y.append(getYEntry(G))


# dimacs
stem = 'https://mat.gsia.cmu.edu/COLOR04/INSTANCES/'
dimacs = open('../Data/dimacs_list.txt')
context = ssl._create_unverified_context()

for dimac in tqdm(dimacs):
    #print(dimac)
    with contextlib.closing(urllib.request.urlopen(stem + dimac, context = context)) as u:
        G = parseDimacGraph(u)
        X.append(getXEntry(G))
        y.append(getYEntry(G))
dimacs.close()

write_X = open('./train_X', 'w')
write_y = open('./train_y', 'w')

for x in X:
    write_X.write(str(x) + '\n')

for i in y:
    write_y.write(str(i) + '\n')

write_X.close()
write_y.close()