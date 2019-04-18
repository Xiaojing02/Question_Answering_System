
import numpy as np
import os
from collections import Counter
from nltk.corpus import stopwords

import spacy


nlp = spacy.load('en_core_web_sm')


path = "./WikipediaArticles"


# print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
#                   token.shape_, token.is_alpha, token.is_stop)

countMap = {}
for fileName in os.listdir(path):
    if fileName.endswith(".txt"):
        f = open(path + "/" + fileName, "r", encoding="ISO-8859-1")
        read_data = f.read()
        f.seek(0)
        for line in f:
            if len(line) > 1:
                sentencesSplit = line.split(". ")

        doc = nlp(read_data)
        # tokens = read_data.split()
        stopWords = set(stopwords.words('english'))
        tokens = []
        for token in doc:
            if token.lemma_ not in stopWords and not token.is_punct and token.lemma_ != "-PRON-":
                tokens.append(token.lemma_)
        N = len(tokens)
        cnt = Counter(tokens)
        # for item in cnt:
        #     cnt[item] /= N
        # print(cnt)
        #
        # input_sentence = "When was UTD established?"
        # doc2 = nlp(input_sentence)
        # p = 1
        # for token in doc2:
        #     if token.lemma_ not in stopWords and not token.is_punct and token.lemma_ != "-PRON-":
        #         if cnt[token.lemma_] != 0:
        #             p = p * cnt[token.lemma_]
        #         else:
        #             p = p * (1 / N)
        # print(fileName, p)

        input_sentence = "Who founded Apple Inc.?"
        doc2 = nlp(input_sentence)
        sumOfAppearance = 0
        for token in doc2:
            if token.lemma_ not in stopWords and not token.is_punct and token.lemma_ != "-PRON-":
                for item in cnt:
                    if item in token.lemma_:
                        sumOfAppearance += cnt[item]
        print(fileName, sumOfAppearance)
