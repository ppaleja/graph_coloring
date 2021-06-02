import urllib.request
import contextlib
import ssl
import wget

from tqdm import tqdm

#from tqdm import tqdm
stem = 'https://mat.gsia.cmu.edu/COLOR04/INSTANCES/'
dimacs = open('../Data/dimacs_list.txt')
context = ssl._create_unverified_context()

for dimac in tqdm(dimacs):
    #print(dimac)
    #url = stem + dimac
    #wget.download(url, './dimacs/' + dimac.strip())
    with contextlib.closing(urllib.request.urlopen(stem + dimac, context = context)) as u:
        f = open('./dimacs/' + dimac.strip(), 'bw')
        datatowrite = u.read()
        f.write(datatowrite)
        f.close()

    