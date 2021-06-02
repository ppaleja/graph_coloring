import subprocess
import os
import re

from tqdm import tqdm
#from  import *
import networkx as nx
import pandas as pd
#from my_ils import *
#from my_tabu import *

import copy
import random
import os
algs = ['AntCol', 'BacktrackingDSatur', 'HillClimber', 'HybridEA', 'PartialColAndTabuCol', 'RLF', 'SimpleGreedy']
datas = [{
        'clique_size': [],
        'num_cliques': [],
        'chr_num': [],
        'clrs_fnd': [],
        'time_taken': [],
        'num_improved': []
    }] * 7

for clique_size in range(0, 21, 5)[1:]:
    data = {
        'alg': [],
        'clique_size': [],
        'num_cliques': [],
        'chr_num': [],
        'clrs_fnd': [],
        'time_taken': [],
        'checks': [],
        'num_improved': []
    }

# Now, lets try ranging over 200 to 300
    for num_cliques in tqdm(range(1, 300)):
        filename = 'var_clique_sizes_graphs/' + str(clique_size) + '_' + str(num_cliques)
        p_write = subprocess.Popen(
            ['./generator', filename],
            stdin = subprocess.PIPE,
            stdout = subprocess.PIPE
        )
        p_write.communicate(
            str('0\n' +
            '1\n' + 
            '3\n' +
            '500\n' +
            '20\n' +
            '10\n' +
            '5\n' +
            '0\n' +
            str(num_cliques) + '\n' +
            str(clique_size) + '\n' +
            '0\n' +
            '0\n' +
            '1\n').encode()
        )
        for i, alg in enumerate(algs):
            #data = datas[i]
            p_test = subprocess.Popen(
                ['../../Code/readymade_heuristics/gCol/' + alg + '/' + alg, filename, '-v'],
                #['./' + alg + '/' + alg, stem + curr_dataset + '/' + graph, '-v'],
                #stdin = subprocess.PIPE,
                stdout = subprocess.PIPE
            )

            start = -1
            last_arr = []
            for line in p_test.stdout:
                arr = line.decode().strip().split()
                #print(arr)
                if 'COLS' in arr:
                    start = 0
                elif start > -1 and arr:
                    start += 1
                    arr[1] = int(arr[1].split('m')[0])
                    #print(arr)
                    last_arr = list(map(int, arr[:3]))
                elif not arr and start > -1:
                    break
            if not last_arr:
                print('Some error happpend with alg {}, clique size {}, clique number {}'.format(alg, clique_size, num_cliques))
                continue

            data['alg'].append(alg)
            data['num_cliques'].append(num_cliques)
            data['clique_size'].append(clique_size)
            data['chr_num'].append(20)
            data['clrs_fnd'].append(last_arr[0])
            data['time_taken'].append(last_arr[1])
            data['checks'].append(last_arr[2])
            data['num_improved'].append(start)

            p_test.kill()
        p_write.kill()

    pd.DataFrame(data=data).to_csv('var_clique_sizes_results/' + 'all-algs' + '_chr20_clqsiz' + str(clique_size) + '_data.csv')
"""      
for i, alg in enumerate(algs):
    # Convert to pandas df
    df = pd.DataFrame(data=datas[i])
    df.to_csv('const_cliq_size_results/' + alg + '_chr20_clq1-300_data.csv')
        # Now, I think we want to write our results....
"""

