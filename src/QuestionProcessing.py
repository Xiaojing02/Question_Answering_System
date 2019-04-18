import nltk
import string
import FeatureExtraction as fe
import sys
from collections import Counter


def get_keywords(sentence):
    # tokens = fe.get_words(sentence)
    # count = Counter(tokens)
    # return count.most_common(10)
    # return fe.get_words_and_synonyms(sentence)
    # return fe.get_words(sentence)
    return fe.get_word_set_using_spacy(sentence)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        num = len(sys.argv) - 1
        print(sys.argv[0] + ": got " + str(num)
              + " arguments. Expecting:[A question]")
        exit()

    sent = sys.argv[1]
    print(get_keywords(sent))
