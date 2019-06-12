import re
import json

result_sentences = set()
end_ = ['?', '!', '.', '。']

f_sentences = open("txt/sentences_life.txt", 'wt')

f_news = open("txt/news-life-0531.json", 'r')
data = json.loads(f_news.read())
f_news.close()

for news in data:
    txt = news['news_txt']
    parttern = "“(.*?)”"
    result = re.findall(parttern, txt)
    sentences = [sentence for sentence in result if sentence != '' and sentence[-1] in end_]
    for sentence in sentences:
        #f_sentences.write(sentence + '\n')
        result_sentences.add(sentence)
        print("Get life-sentence: '{}'".format(sentence))
for sentence in result_sentences:
    f_sentences.write(sentence + '\n')

f_sentences.close()

'''
f_sentences = open("txt/sentences_ecnomic.txt", 'wt')
f_news = open("txt/news-ecnomic-0531.json", 'r')
data = json.loads(f_news.read())
f_news.close()

for news in data:
    txt = news['news_txt']
    parttern = "“(.*?)”"
    result = re.findall(parttern, txt)
    sentences = [sentence for sentence in result if len(sentence) > 1 and sentence[-1] in end_]
    for sentence in sentences:
        #f_sentences.write(sentence + '\n')
        result_sentences.add(sentence)
        print("Get ecnomic-sentence: '{}'".format(sentence))

for sentence in result_sentences:
    f_sentences.write(sentence + '\n')

f_sentences.close()
'''