import re
from collections import defaultdict

import jieba
import numpy as np
from jieba import posseg

class DictClassifier:
    """docstring for DictClassifier"""
    def __init__(self):
        self.__root_filepath = "dict/"

        jieba.load_userdict("dict/user2.dict")

        self.__positive_dict = self.__get_dict(self.__root_filepath + "positive_dict.txt")
        self.__negative_dict = self.__get_dict(self.__root_filepath + "negative_dict.txt")
        self.__conjunction_dict = self.__get_dict(self.__root_filepath + "conjunction_dict.txt")
        self.__punctuation_dict = self.__get_dict(self.__root_filepath + "punctuation_dict.txt")
        self.__adverb_dict = self.__get_dict(self.__root_filepath + "adverb_dict.txt")
        self.__denial_dict = self.__get_dict(self.__root_filepath + "denial_dict.txt")

    def classify(self, sentence):
        return self.analyse_sentence(sentence)

    def analyse_sentence(self, sentence):
        sentence_analysis = {
            "score": 0
        }

        the_clauses = self.__divide_sentence_into_clauses(sentence + '%')

        for i in range(len(the_clauses)):
            #print("__analyse_clause[{}]: {}".format(i,the_clauses[i].replace("。", ".")))
            sub_clause = self.__analyse_clause(the_clauses[i].replace("。", "."))

            sentence_analysis["su-clause" + str(i)] = sub_clause
            sentence_analysis["score"] += sub_clause["score"]

        if sentence_analysis["score"] > 0:
            return sentence_analysis["score"]
        else:
            return sentence_analysis["score"]

    def __analyse_clause(self, the_clause):
        sub_clause = {
            "score": 0,
            "positive": [],
            "negative": [],
            "conjunction": [],
            "punctuation": [],
            "pattern": []
        }
        seg_result = posseg.lcut(the_clause)

        '''
        if runout_filepath is not None:
            self.__write_runout_file(runout_filepath, the_clause + '\n')
            self.__write_runout_file(runout_filepath, str(seg_result) + '\n')
        if print_show:
            print(the_clause)
            print(seg_result)
        '''

        for i in range(len(seg_result)):
            mark, result = self.__analyse_word(seg_result[i].word, seg_result, i)
            #print('word({})result:{}type:{}'.format(seg_result[i].word, result, mark))
            if mark == 0:
                continue
            elif mark == 1:
                sub_clause["conjunction"].append(result)
            elif mark == 2:
                sub_clause["punctuation"].append(result)
            elif mark == 3:
                sub_clause["positive"].append(result)
                sub_clause["score"] += result["score"]
            elif mark == 4:
                sub_clause["negative"].append(result)
                sub_clause["score"] -= result["score"]

        #综合连词的情感值
        for a_conjunction in sub_clause["conjunction"]:
            sub_clause["score"] *= a_conjunction["value"]

        #综合标点符号情感值
        for a_punctuation in sub_clause["punctuation"]:
            sub_clause["score"] *= a_punctuation["value"]

        return sub_clause


    def __analyse_word(self, the_word, seg_result=None, index=-1):
        #连词
        judgement = self.__is_word_conjunction(the_word)
        if judgement != '':
            return 1, judgement

        #标点符号
        judgement = self.__is_word_punctuation(the_word)
        if judgement != '':
            return 2, judgement

        #positive word
        judgement = self.__is_word_positive(the_word, seg_result, index)
        if judgement != '':
            return 3, judgement

        #negative word
        judgement = self.__is_word_negative(the_word, seg_result, index)
        if judgement != '':
            return 4, judgement

        return 0, ''

    def __is_word_conjunction(self, the_word):
        if the_word in self.__conjunction_dict:
            conjunction = {"key": the_word, "value": self.__conjunction_dict[the_word]}
            return conjunction
        #不在词典内则返回空
        return ''

    def __is_word_punctuation(self, the_word):
        if the_word in self.__punctuation_dict:
            punctuation = {
                "key": the_word,
                "value": self.__punctuation_dict[the_word]
            }
            return punctuation
        #不在词典内则返回空
        return ''

    def __is_word_positive(self, the_word, seg_result, index):
        if the_word in self.__positive_dict:
            return self.__emotional_word_analysis(the_word, self.__positive_dict[the_word], [x for x, y in seg_result], index)
        return ''

    def __is_word_negative(self, the_word, seg_result, index):
        if the_word in self.__negative_dict:
            return self.__emotional_word_analysis(the_word, self.__negative_dict[the_word], [x for x, y in seg_result], index)
        return ''

    def __emotional_word_analysis(self, core_word, value, segments, index):
        #在情感词典内则构建一个以情感词典为中心的字典数据结构
        orientation = {
            "key": core_word,
            "adverb": [],
            "denail": [],
            "value": value
        }
        orientation_score = orientation["value"]

        #在前三个视窗内判断是否有否定词，副词
        view_window = index - 1
        if view_window > -1: #无越界
            #判断前一个词是否是情感词
            if segments[view_window] in self.__negative_dict or segments[view_window] in self.__positive_dict:
                orientation["score"] = orientation_score
                return orientation
            #判断是否是副词
            if segments[view_window] in self.__adverb_dict:
                adverb = {
                    "key": segments[view_window],
                    "position":1,
                    "value":self.__adverb_dict[segments[view_window]]
                }
                orientation["adverb"].append(adverb)
                orientation_score *= self.__adverb_dict[segments[view_window]]
            elif segments[view_window] in self.__denial_dict: #判断是否是否定词
                denail = {
                    "key": segments[view_window],
                    "position": 1,
                    "value": self.__denial_dict[segments[view_window]]
                }
                orientation["denail"].append(denail)
                orientation_score *= -1
        view_window = index -2
        if view_window > -1:
            # 判断前一个词是否是情感词
            if segments[view_window] in self.__negative_dict or segments[view_window] in self.__positive_dict:
                orientation['score'] = orientation_score
                return orientation
            if segments[view_window] in self.__adverb_dict:
                adverb = {"key": segments[view_window], "position": 2,
                          "value": self.__adverb_dict[segments[view_window]]}
                orientation_score *= self.__adverb_dict[segments[view_window]]
                orientation["adverb"].insert(0, adverb)
            elif segments[view_window] in self.__denial_dict:
                denial = {"key": segments[view_window], "position": 2,
                          "value": self.__denial_dict[segments[view_window]]}
                orientation["denial"].insert(0, denial)
                orientation_score *= -1
                # 判断是否是“不是很好”的结构（区别于“很不好”）
                if len(orientation["adverb"]) > 0:
                    # 是，则引入调节阈值，0.3
                    orientation_score *= 0.3
        view_window = index - 3
        if view_window > -1:
            # 判断前一个词是否是情感词
            if segments[view_window] in self.__negative_dict or segments[view_window] in self.__positive_dict:
                orientation['score'] = orientation_score
                return orientation
            if segments[view_window] in self.__adverb_dict:
                adverb = {"key": segments[view_window], "position": 3,
                          "value": self.__adverb_dict[segments[view_window]]}
                orientation_score *= self.__adverb_dict[segments[view_window]]
                orientation["adverb"].insert(0, adverb)
            elif segments[view_window] in self.__denial_dict:
                denial = {"key": segments[view_window], "position": 3,
                          "value": self.__denial_dict[segments[view_window]]}
                orientation["denial"].insert(0, denial)
                orientation_score *= -1
                # 判断是否是“不是很好”的结构（区别于“很不好”）
                if len(orientation["adverb"]) > 0 and len(orientation["denial"]) == 0:
                    orientation_score *= 0.3
        orientation["score"] = orientation_score
        return orientation

    def __divide_sentence_into_clauses(self, the_sentence):
        the_clauses = self.__split_sentence(the_sentence)

        #识别＂是...不是．．．＂句式
        pattern = re.compile(r"([，、。%！；？?,!～~.… ]*)([\u4e00-\u9fa5]*?(是).+(不是)[\u4e00-\u9fa5]+?[，。！%；、？?,!～~.… ]+)")

        match = re.search(pattern, the_sentence.strip())
        if match is not None and len(self.__split_sentence(match.group(2))) <=2:
            to_delete = []
            for i in range(len(the_clauses)):
                if the_clauses[i] in match.group(2):
                    to_delete.append(i)
                if len(to_delete) > 0:
                    for i in range(len(to_delete)):
                        the_clauses.remove(the_clauses[to_delete[0]])
                            #the_clauses[to_delete[i]]
                    the_clauses.insert(to_delete[0], match.group(2))

        pattern = re.compile(r"([，%。、！；？?,!～~.… ]*)([\u4e00-\u9fa5]*?(如果|要是|希望).+就[\u4e00-\u9fa5]+(好|完美)了[，。；！%、？?,!～~.… ]+)")
        match = re.search(pattern, the_sentence.strip())
        if match is not None and len(self.__split_sentence(match.group(2))) <= 3:
            to_delete = []
            for i in range(len(the_clauses)):
                if the_clauses[i] in match.group(2):
                    to_delete.append(i)
            if len(to_delete) > 0:
                for i in range(len(to_delete)):
                    the_clauses.remove(the_clauses[to_delete[0]])
                the_clauses.insert(to_delete[0], match.group(2))

        the_clauses[-1] = the_clauses[-1][:-1]
        return the_clauses



    @staticmethod
    def __split_sentence(sentence):
        pattern = re.compile(r"[，。%、！!？?,；～~.… ]+")

        split_clauses = pattern.split(sentence.strip())
        paunctuations = pattern.findall(sentence.strip())
        try:
            split_clauses.remove('')
        except ValueError:
            pass
        paunctuations.append('')

        clauses = [''.join(x) for x in zip(split_clauses, paunctuations)]

        return clauses

    @staticmethod
    def __get_dict(path, encoding="utf-8"):
        sentiment_dict = {}
        pattern = re.compile(r"\s+")
        with open(path, encoding=encoding) as f:
            for line in f:
                result = pattern.split(line.strip())
                if len(result) == 2:
                    sentiment_dict[result[0]] = float(result[1])
        return sentiment_dict

if __name__ == "__main__":
    pass