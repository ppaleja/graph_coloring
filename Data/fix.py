#from tqdm import tqdm

datasets = ['testset'] #['chi1000', 'chi500', 'dimacs', 'testset']
for curr_dataset in datasets:
    stem = curr_dataset
    graphsToUse = []
    graphFile = open(str(stem + '_list.txt'))
    for line in graphFile:
        graphsToUse.append(line.strip())
    graphFile.close()

    for i, filename in enumerate(graphsToUse):
        print(i)
        f = open('./testset/' + filename)
        new_f = open('./testset_fixed/' + filename, 'wb')
        for line in f:
            if line[0] == 'c':
                new_f.write(line.strip() + '\n')
            elif line[0] == 'e':
                new_f.write(line.strip() + '\n')
            elif line[0] == 'p':
                new_f.write(line.strip().replace('col', 'edge') + '\n')
        f.close()
        new_f.close()
