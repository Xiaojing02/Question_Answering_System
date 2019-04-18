import sys
import os
from os import listdir
from os.path import isfile, join
import collections
import FeatureExtraction as fe
import PickleUtils as pu
from Sentence import Sentence
from Document import Document
import spacy
from nltk.corpus import stopwords


document_db = {}


# use spaCy processing pipeline to process original documents
def preprocess(file, filename):
    doc_name = filename.split("/")[-1]
    word_set = fe.get_word_set_using_spacy(file)
    doc = Document(doc_name)
    document_db[doc] = word_set


if __name__ == "__main__":
    if len(sys.argv) != 3:
        num = len(sys.argv) - 1
        print(sys.argv[0] + ": got " + str(num)
              + "arguments. Expecting:[corpus_folder] and [pickle_folder]")
        exit()

    folder = sys.argv[1]
    if folder[-1] != "/":
        folder = folder + "/"
    files = [join(folder, f) for f in listdir(folder) if isfile(join(folder, f))]
    for file in files:
        print(file)
        if file.endswith(".txt"):
            f = open(file, "r")
            preprocess(f, file)
    destination = sys.argv[2]
    if destination[-1] != "/":
        destination = destination + "/"
    pu.storeData(database, destination + "database.pickle")


