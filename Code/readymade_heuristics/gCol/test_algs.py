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


for alg in ['AntCol', 'BacktrackingDSatur', 'HillClimber', 'HybridEA', 'PartialColAndTabuCol', 'RLF', 'SimpleGreedy']:

    datasets = ['chi500', 'dimacs_fixed', 'testset_fixed']#['chi1000', 'chi500', 'dimacs_fixed', 'testset_fixed']
    for curr_dataset in datasets:
        if alg == 'AntCol' and curr_dataset == 'chi500': continue
        y = []
        stem = '../../../Data/'
        graphsToUse = []
        graphFile = open(str(stem + curr_dataset + '_list.txt'))
        for line in graphFile:
            graphsToUse.append(line.strip())
        graphFile.close()

        
        for graph in tqdm(graphsToUse, 'Running on ' + alg):
            p = subprocess.Popen(
                ['./' + alg + '/' + alg, stem + curr_dataset + '/' + graph, '-v'],
                #stdin = subprocess.PIPE,
                stdout = subprocess.PIPE
            )
            start = -1
            last_arr = []
            for line in p.stdout:
                arr = line.decode().strip().split()
                #print(arr)
                if 'COLS' in arr:
                    start = 0
                elif start == 0 and arr:
                    arr[1] = int(arr[1].split('m')[0])
                    #print(arr)
                    last_arr = list(map(int, arr[:3]))
                elif not arr and start == 0:
                    start = -1
                    break
            y.append(last_arr)
                # if(arr) and start == 2:
                #     print(arr)
                #     arr[1] = int(arr[1].split('m')[0])
                #     #print(arr)
                #     last_arr = list(map(int, arr))
                # elif start == -1:
                #     start = 0
                # elif start == 0:
                #     start = 1
                # elif start == 1:
                #     start = 2
                # elif start == 2:
                #     y.append(tuple(last_arr))
                #     #print(tuple(last_arr, alg))
                #     break
            p.kill()
        
        write_y = open(str('./measurements/' + alg + '/' + curr_dataset + '_y'), 'w')
        write_y.write('Colors, Time, Iterations\n')

        for i in y:#tqdm(y):
            write_y.write(str(i) + '\n')
        write_y.close()
        