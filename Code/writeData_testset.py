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

from utils import getGreedyCliques, greedyClique, parseGraph, getXEntry, getYEntry

Path = 'Data/testset/'

X = []
y = []

filelist = os.listdir(Path)
for i in tqdm(filelist):
    if i.endswith(".col"):
        G = parseGraph(Path + i)
        X.append(getXEntry(G))
    #y.append(getYEntry(G))

write_X = open('Data/clique_measurements/test_X', 'w')
#write_y = open('./test_y', 'w')

for x in X:
    write_X.write(str(x) + '\n')

#for i in y:
  #  write_y.write(str(i) + '\n')

write_X.close()
#write_y.close()