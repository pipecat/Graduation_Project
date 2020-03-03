from classifiers import DictClassifier
f_now_in = "txt/xi.txt"
f_now_out = "txt/sentences_corpus_xi.txt"


ds = DictClassifier()
f_in = open(f_now_in, 'r')
f_out = open(f_now_out, 'wt')
for line in f_in:
    result = ds.analyse_sentence(line)
    if result < 0:
        f_out.write('neg ' + line)
    else:
        f_out.write('pos ' + line)
f_in.close()
f_out.close()

