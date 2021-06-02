import time
import numpy as np
import os
import networkx as nx
from collections import deque
import random
from tqdm import tqdm
import gzip
from scipy.stats import variation, entropy
import statistics
import urllib

max_secs = 10

def getGreedyCliques(G):
    cliques = []

    vertices = list(G.nodes)
    for i in range(8):
        random.shuffle(vertices)

    start = time.process_time()
    for v in vertices:
        if time.process_time() - start > 10:
            break
        cliques.append(greedyClique(G, v))
    return cliques

def greedyClique(G, startV):
    clique = [startV]
    for v in G:
        if v in clique:
            continue
        isNext = True
        for u in clique:
            if u in G[v]:
                continue
            else:
                isNext = False
                break
        if isNext:
            clique.append(v)

    return sorted(clique)

def parseGraph(filename):
    # So first we have to cull the thing
    G = nx.Graph()

    f = open(filename)
    for line in f:
        if line[0] == 'c':
            continue
        elif line[0] == 'e':
            x = line.split()
            G.add_edge(int(x[1]) - 1, int(x[2]) - 1)
    f.close()
    for i in range(len(G)):
        if i not in G:
            G.add_node(i)
    return G

def parseDimacGraph(file):
    G = nx.Graph()
    for line in file:
        line = line.split()
        if len(line) == 0 or 'e' not in str(line[0]):
            continue
        else:
            G.add_edge(int((line[1])) - 1, int((line[2])) - 1)
    #print('sheraskdlfl' + str(G))
    return G

def getXEntry(G):

    time_start = time.process_time_ns() 
    cliques = getGreedyCliques(G)       
    computation_time = (time.process_time_ns()  - time_start)

    normalizedCliqueSizes = [len(c) / G.order() for c in cliques]
    normalizedCliqueSizes.sort()
    q1, q3 = np.quantile(normalizedCliqueSizes, [.25, .75])
    var_coef = variation(normalizedCliqueSizes)
    e = entropy(normalizedCliqueSizes)

    max_card = max(normalizedCliqueSizes) * G.order()
    return [
        normalizedCliqueSizes[0], normalizedCliqueSizes[-1], statistics.median(normalizedCliqueSizes),
        var_coef, e, computation_time, max_card
    ]
def getYEntry(G):
    time_start = time.process_time_ns() 
    nx.greedy_color(G, strategy='DSATUR')
    return (time.process_time_ns() - time_start)