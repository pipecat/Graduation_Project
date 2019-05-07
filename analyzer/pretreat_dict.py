f_dict = open("dict/BosonNLP_sentiment_score/BosonNLP_sentiment_score.txt", "r")
f_positive = open("dict/positive_dict2.txt", "wt")
f_negative = open("dict/negative_dict2.txt", "wt")
f_user = open("dict/user2.dict", "wt")

for line in f_dict:
    data = line.strip().split()[0]
    score = float(line.strip().split()[1])
    if score < 0.0:
        f_negative.write(data + ' ' + str(-score) + '\n')
    else:
        f_positive.write(line)
    f_user.write(data + '\n')

f_dict.close()
f_positive.close()
f_negative.close()
f_user.close()