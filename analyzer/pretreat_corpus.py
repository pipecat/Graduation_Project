import jieba

corpus_path = "txt/corpus_xi.txt"
origin_path = "txt/xi.txt"
stop_path = "dict/stopwords.txt"
jieba.load_userdict("dict/user.dict")

stop_words = ['，','、','。','%','！','；','？','?',',','!','～','~','.','…']
with open(stop_path, 'r') as f:
    for line in f:
        stop_words.append(line.strip())

f_origin = open(origin_path, 'r')
f_corpus = open(corpus_path, 'wt')

for line in f_origin:
    pos_or_neg = line.strip().split()[0]
    #print(line)
    sentence = line.strip().split()[1]
    word_list = list(jieba.cut(sentence, cut_all=False))
    for word in word_list:
        if word in stop_words:
            word_list.remove(word)
    word_list.insert(0, pos_or_neg)
    f_corpus.write(' '.join(word_list) + '\n')

f_origin.close()
f_corpus.close()