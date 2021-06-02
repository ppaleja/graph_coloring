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

y = []
# chi1000
datasets = ['dimacs'] #['chi1000', 'chi500', 'dimacs', 'testset']
for curr_dataset in datasets:
    stem = '../../Data/' + curr_dataset
    graphsToUse = []
    graphFile = open(str(stem + '_list.txt'))
    for line in graphFile:
        graphsToUse.append(line.strip())
    graphFile.close()

    for graph in tqdm(graphsToUse):

        # Do Dsatur first
        p = subprocess.Popen(
            ['./bin/dsatur', stem + '/' + graph],
            stdin = subprocess.PIPE,
            stdout = subprocess.PIPE
        )
        d_out = p.communicate(input=
            str('0\n' + 
            '1\n' + 
            '4\n'
            ).encode()
        )
        start = 0
        check = str(d_out[0]).replace('\\t', '\\n')
        for f in check.split('\\n'):
            if 'CLRS =' in f:
                start = int(f.split('=')[1])
                break
        
        # Do Tabu
        p = subprocess.Popen(
        ['./bin/tabu', stem + '/' + graph],
        stdin = subprocess.PIPE,
        stdout = subprocess.PIPE
        )
        t = int(start * .9)
        out = p.communicate(input=
            str('0\n' + 
            '1\n' + 
            '1000\n' + 
            '100\n' + 
            '10\n' + 
            '17\n' + 
            str(t) + '\n' + 
            str(start - t) +'\n' + 
            '1\n')
            .encode())
        #print(str(out[0]))
        check = str(out[0]).replace('\\t', '\\n')
        #print(check)
        #print(check.split('\\n'))
        #for check in out[0].split():
        toAdd = [None, None, None]
        for f in check.split('\\n'):
            if 'CLRS =' in f:
                #print('DSATUR colors:', start)
                #print('Tabu Colors:', f.split('=')[1])
                toAdd[0] = start
                toAdd[1] = int(f.split('=')[1])
            if 'Coloring time cpu = ' in f:
                #print(f.split()[4])
                toAdd[2] = float(f.split()[4])
            if 'Coloring ' in f:
                #print(f)
                pass
        if(toAdd == [None, None, None]):
            """
            p = subprocess.Popen(
                ['./bin/tabu', stem + '/' + graph],
                stdin = subprocess.PIPE,
                #stdout = subprocess.PIPE
                )
            t = int(start * .9)
            p.communicate(input=
                str('0\n' + 
                '1\n' + 
                '1000\n' + 
                '100\n' + 
                '10\n' + 
                '17\n' + 
                str(t) + '\n' + 
                str(start - t) +'\n' + 
                '1\n')
                .encode())
            """
            # So its not my fault that it seg faults lmao
            print(graph)
        y.append(tuple(toAdd))
        print(graph)
        print(toAdd)
    print(len(y))
    """
    write_y = open(str('../jc_measurements/' + curr_dataset + '_y'), 'w')
    write_y.write('DSATUR, TABU, TIME\n')

    for i in tqdm(y):
        write_y.write(str(i) + '\n')
    write_y.close()
    

"""