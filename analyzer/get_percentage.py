file_path = "txt/sentences_corpus_life.txt"
num = 0
p_num = 0
n_num = 0
with open(file_path, 'r') as f:
    for line in f:
        num += 1
        if line[0] == 'p':
            p_num += 1
        elif line[0] == 'n':
            n_num += 1
print('p_num:{}'.format(p_num))
print('n_num:{}'.format(n_num))