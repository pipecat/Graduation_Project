from classifiers import BayesClassifier, DictClassifier
from feature_extraction import ChiSquare
from tools import get_data_and_labels
import jieba
import time


#jieba.load_userdict("dict/user.dict") 

def test_dict():
    file_path = "txt/sentences_corpus.txt"
    data = []
    with open(file_path, 'r') as f:
        for line in f:
            sentence = line.strip().split()[1]
            polar = line.strip().split()[0]
            item = { 'sentence': sentence }
            if polar == 'pos':
                item['real_polar'] = 1
            else:
                item['real_polar'] = 0
            data.append(item)
    correct_num = 0
    pos_num = 0
    num = len(data)
    ds = DictClassifier()
    start = time.clock()
    for i, item in enumerate(data):
        #test_score = ds.analyse_sentence(item['sentence'])
        try:
            test_score = ds.analyse_sentence(item['sentence'])
        except Exception as e:
            #print("Error sentence:{}".format(item['sentence']))
            raise e
        data[i]['test_score'] = test_score
        if test_score >= -1:
            pos_num += 1
        if test_score <= -1 and item['real_polar'] == 0:
            data[i]['test_result'] = True
            correct_num += 1
        elif test_score > -1 and item['real_polar'] == 1:
            data[i]['test_result'] = True
            correct_num += 1
        else:
            data[i]['test_result'] = False
            #print("Error sentence:{}\nreal_polar:{}  test_result:{}".format(item['sentence'], item['real_polar'], test_score))
    end = time.clock()
    print('Use time {}s'.format(end-start))
    print('Correct percentage of DictClassifier:{}'.format(correct_num/num))
    print(' Pos percentage of DictClassifier:{}'.format(pos_num/num))
    sentences = sorted(data, key=lambda item:item['test_score'], reverse=True)
    #return [item for item in sentences[:500] if len(item['sentence']) < 30]


def test_bayes():
    train_file_path = "txt/corpus.txt"
    test_file_path = "txt/test_corpus.txt"
    data = []
    with open(test_file_path, 'r') as f:
        for line in f:
            #print(line)
            sentence = line.strip().split()[:-1]
            polar = line.strip().split()[0]
            item = { 'sentence': sentence }
            if polar == 'pos':
                item['real_polar'] = 1
            else:
                item['real_polar'] = 0
            data.append(item)
    correct_num = 0
    pos_num = 0
    num = len(data)
    sentences, labels = get_data_and_labels(2000, train_file_path)
    fe = ChiSquare(sentences, labels)
    best_words = fe.best_words(1000)
    bayes = BayesClassifier(sentences, labels, best_words=best_words)
    start = time.clock()
    for i, item in enumerate(data):
        #test_score = bayes.analyse_sentence(item['sentence'])
        try:
            test_score = bayes.classify(item['sentence'])
        except Exception as e:
            #print("Error sentence:{}".format(item['sentence']))
            raise e
        data[i]['test_score'] = test_score
        if test_score == 1:
            pos_num += 1
        if test_score == 0 and item['real_polar'] == 0:
            data[i]['test_result'] = True
            correct_num += 1
        elif test_score == 1 and item['real_polar'] == 1:
            data[i]['test_result'] = True
            correct_num += 1
        else:
            data[i]['test_result'] = False
            #print("Error sentence:{}\nreal_polar:{}  test_result:{}".format(item['sentence'], item['real_polar'], test_score))
    end = time.clock()
    print('Use time {}s'.format(end-start))
    print('Correct percentage of BayesClassifier:{}'.format(correct_num/num))
    print('Pos percentage of BayesClassifier:{}'.format(pos_num/num))