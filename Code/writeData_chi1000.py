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
import urllib
import contextlib

from utils import getGreedyCliques, greedyClique, parseGraph, getXEntry, getYEntry


X = []
y = []

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

"""
filelist = os.listdir(Path)
for i in tqdm(filelist):
    if i in graphsToUse:
        G = parseGraph(Path + i)
        X.append(getXEntry(G))
        y.append(getYEntry(G))
"""

write_X = open('./chi1000_X', 'w')
write_y = open('./chi1000_y', 'w')

for x in X:
    write_X.write(str(x) + '\n')

for i in y:
    write_y.write(str(i) + '\n')

write_X.close()
write_y.close()