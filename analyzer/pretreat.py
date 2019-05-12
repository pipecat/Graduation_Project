import re
import json

result_sentences = set()
end_ = ['?', '!', '.', '。']

f_sentences = open("txt/sentences.txt", 'wt')

f_news = open("txt/news-0502.json", 'r')
data = json.loads(f_news.read())
f_news.close()

for news in data:
    txt = news['news_txt']
    parttern = "“(.*?)”"
    result = re.findall(parttern, txt)
    sentences = [sentence for sentence in result if sentence[-1] in end_]
    for sentence in sentences:
        #f_sentences.write(sentence + '\n')
        result_sentences.add(sentence)
        print("Get sentence: '{}'".format(sentence))

f_news = open("txt/news-0504.json", 'r')
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
        print("Get sentence: '{}'".format(sentence))

for sentence in result_sentences:
    f_sentences.write(sentence + '\n')

f_sentences.close()