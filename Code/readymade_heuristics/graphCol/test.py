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
import gc

CPN_IDX = 0
NPC_IDX = 1

y = []
# chi1000
datasets = ['chi500'] #['chi1000', 'chi500', 'dimacs', 'testset']
for curr_dataset in datasets:
    stem = 'instances/'
    graphsToUse = []
    graphFile = open(str(stem + curr_dataset + '_list.txt'))
    for line in graphFile:
        graphsToUse.append(line.strip())
    graphFile.close()

    for graph in tqdm(graphsToUse):
        gc.collect()
        p = subprocess.Popen(
            ['./color', stem + graph],
            stdin = subprocess.PIPE,
            stdout = subprocess.PIPE
        )
        # So we need to find the last line, I think
        line = p.stdout.readline()
        while True:
            t = p.stdout.readline()
            if not t:
                print(line)
                break
            else:
                line = t

        #for line in tqdm(p.stdout):

        p.kill()
        #break
        #exit()
        """
        t = open(str('./test_' + graph + '_y'), 'wb')
        for line in tqdm(p.stdout):
            #line = p.stdout.readline()
            print(line)
            t.write(line)
            #the real code does filtering here
            #print "test:", line.rstrip()
        t.close()
        exit()"""
    print('here')