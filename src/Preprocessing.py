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


def get_paragraphs(document):
    paragraphs = document.split("\n\n")
    return paragraphs


def calc_ti_idf_vector(document):
    paragraphs = get_paragraphs(document)
    # print("Num of paragraph: " + str(len(paragraphs)))
    tfidf, tfs = fe.get_tf_idf(paragraphs)
    return paragraphs, tfidf, tfs
