import nltk
import string
import FeatureExtraction as fe
import sys
from collections import Counter


def get_keywords(sentence):
    return fe.get_word_set_using_spacy(sentence)

