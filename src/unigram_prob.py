
import numpy as np
import os
from collections import Counter
from nltk.corpus import stopwords

import spacy


nlp = spacy.load('en_core_web_sm')


path = "./WikipediaArticles"


# print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
#                   token.shape_, token.is_alpha, token.is_stop)

for fileName in os.listdir(path):
    if fileName.endswith(".txt"):
        sentences = []
        f = open(path + "/" + fileName, "r", encoding="ISO-8859-1")
        read_data = f.read()
        f.seek(0)
        for line in f:
            if len(line) > 1:
                sentencesSplit = line.split(". ")
                sentences.extend(sentencesSplit)

        doc = nlp(read_data)
        # tokens = read_data.split()
        stopWords = set(stopwords.words('english'))
        tokens = []
        for token in doc:
            if token.lemma_ not in stopWords and not token.is_punct and token.lemma_ != "-PRON-":
                tokens.append(token.lemma_)
        N = len(tokens)
        cnt = Counter(tokens)
        for item in cnt:
            cnt[item] /= N
        # print(cnt)

        input_sentence = "When did Warren Buffett buy Berkshire Hathaway's shares?"
        doc2 = nlp(input_sentence)
        p = 1
        for token in doc2:
            if token.lemma_ not in stopWords and not token.is_punct and token.lemma_ != "-PRON-":
                p = p * cnt[token.lemma_]
        print(fileName, p)

