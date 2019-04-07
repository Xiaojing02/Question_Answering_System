import nltk
from nltk import word_tokenize, sent_tokenize
import sys
import os
from os import listdir
from os.path import isfile, join
from nltk.stem import WordNetLemmatizer
from nltk.corpus import treebank


def preprocess(context):
    sentences = sent_tokenize(context)
    # print(sentences)
    lemmatizer = WordNetLemmatizer()
    for sentence in sentences:
        tokens = word_tokenize(sentence)
        # print(tokens)
        for token in tokens:
            Lemmatize_words = lemmatizer.lemmatize(token)
        tagged = nltk.pos_tag(tokens)
        # print(tagged[0:6])
        entities = nltk.chunk.ne_chunk(tagged)
        print(entities)
        t = treebank.parsed_sents('wsj_0001.mrg')[0]
        t.draw()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        num = len(sys.argv) - 1
        print(sys.argv[0] + ": got " + num
              + "arguments. Expecting 1:[corpus_folder]")
        exit()

    folder = sys.argv[1]
    if folder[-1] != "/":
        folder = folder + "/"
    files = [join(folder, f) for f in listdir(folder) if isfile(join(folder, f))]
    for file in files:
        print(file)
        if file.endswith(".txt"):
            f = open(file, "r")
            preprocess(f.read())
