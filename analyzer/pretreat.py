import re
import json

f_news = open("news-0502.json", 'r')
data = json.loads(f_news.read())
f_news.close()

f_sentences = open("sentences.txt", 'wt')

end_ = ['?', '!', '.', '。']
for news in data:
    txt = news['news_txt']
    parttern = "“(.*?)”"
    result = re.findall(parttern, txt)
    sentences = [sentence for sentence in result if sentence[-1] in end_]
    for sentence in sentences:
        f_sentences.write(sentence + '\n')
        print("Get sentence: '{}'".format(sentence))

f_sentences.close()