import nltk
import string
import FeatureExtraction as fe
import Preprocessing as pp
import sys
from collections import Counter
from nltk.tag import StanfordNERTagger


WH_words = ['how', 'what', 'where', 'when', 'who', 'which']


def extract_wh_word(words):
    for word in words:
        if word.lower() in WH_words or word.lower() == 'whom':
            return word.lower()
    return -1


'''  identify question types based on rules
    return ranked ner tags and classified type
'''


def identify_question_type(wh, q_words):
    lower = pp.lower_tokens(q_words)
    # open_words = self.dataProcessor.remove_stop_words(lower)
    raw_q_sent = ' '.join(lower)
    if 'rank' in raw_q_sent:
        return ['ORDINAL'], 'rank'
    elif 'average' in raw_q_sent:
        return ['NUMBER', 'MONEY'], 'average'
    elif wh == 'what':
        if 'what century' in raw_q_sent:
            return ['ORDINAL'], 'century'
        if 'what language' in raw_q_sent:
            return ['NATIONALITY'], 'language'
        if 'nationality' in raw_q_sent:
            return ['NATIONALITY', 'PERSON'], 'nationality'
        if 'length' in raw_q_sent:
            return ['NUMBER'], 'length'
        if 'what year' in raw_q_sent:
            return ['DATE'], 'year'
        if 'what date' in raw_q_sent:
            return ['DATE'], 'date'
        if 'what percent' in raw_q_sent or 'what percentage' in raw_q_sent:
            return ['PERCENT'], 'percentage'
        if 'number' in raw_q_sent:
            return ['NUMBER'], 'number'
        if 'in what place' in raw_q_sent:
            return ['ORDINAL'], 'order'
        if 'what country' in raw_q_sent:
            return ['COUNTRY'], 'country'
        if 'what city' in raw_q_sent:
            return ['STATE_OR_PROVINCE', 'CITY', 'LOCATION'], 'city'
        if 'what region' in raw_q_sent:
            return ['NATIONALITY'], 'region'
        if 'location' in raw_q_sent:
            return ['LOCATION'], 'place'
        if 'population' in raw_q_sent:
            return ['PERCENT', 'NUMBER'], 'population'
        if 'fraction' in raw_q_sent:
            return ['ORDINAL'], 'fraction'
        if 'what age' in raw_q_sent:
            return ['NUMBER'], 'age'
        if 'what decade' in raw_q_sent:
            return ['DATE'], 'decade'
        if 'temperature' in raw_q_sent:
            return ['NUMBER'], 'temperature'
        if 'abundance' in raw_q_sent:
            return ['PERCENT'], 'abundance'
        if 'capacity' in raw_q_sent:
            return ['NUMBER'], 'capacity'
        else:
            return ['O', 'OTHER', 'PERSON', 'LOCATION', 'NUMBER'], 'else'
    elif wh == 'when':
        return ['DATE', 'TIME', 'NUMBER'], 'time'
    elif wh == 'who' or wh == 'whom':
        return ['PERSON', 'ORGANIZATION', 'OTHER'], 'person'
    elif wh == 'where':
        if 'headquarter' in raw_q_sent or 'capital' in raw_q_sent:
            return ['CITY'], 'headquarter'
        return ['LOCATION', 'ORDINAL', 'OTHER'], 'location'
    elif wh == 'how':
        if 'old' in raw_q_sent or 'large' in raw_q_sent:
            return ['NUMBER'], 'number'
        elif 'how long' in raw_q_sent:
            return ['DURATION', 'NUMBER'], 'length'
        elif 'how far' in raw_q_sent or 'how fast' in raw_q_sent:
            return ['NUMBER', 'TIME', 'PERCENT'], 'length'
        elif 'how many' in raw_q_sent:
            return ['NUMBER'], 'times'
        elif 'how much money' in raw_q_sent:
            return ['MONEY', 'PERCENT', 'NUMBER'], 'money'
        elif 'how much' in raw_q_sent:
            return ['MONEY', 'PERCENT', 'NUMBER'], 'money'
        elif 'how tall' in raw_q_sent:
            return ['number'], 'tall'
        else:
            return ['O', 'NUMBER', 'LOCATION', 'PERSON', 'ORGANIZATION'], 'else'
    elif wh == 'which':
        if 'which language' in raw_q_sent:
            return ['NATIONALITY'], 'language'
        if 'which year' in raw_q_sent:
            return ['TIME', 'NUMBER'], 'year'
        if 'which country' in raw_q_sent:
            return ['COUNTRY'], 'country'
        if 'which city' in raw_q_sent:
            return ['CITY'], 'country'
        if 'place' in raw_q_sent or 'location' in raw_q_sent or 'site' in raw_q_sent:
            return ['LOCATION', 'ORGANIZATION', 'OTHER', 'PERSON'], 'place'
        if 'person' in raw_q_sent:
            return ['PERSON', 'ORGANIZATION', 'OTHER', 'LOCATION'], 'person'
        else:
            return ['O', 'OTHER', 'LOCATION', 'PERSON', 'NUMBER'], 'else'
    elif 'activism' in raw_q_sent or 'philosophy' in raw_q_sent or 'ideology' in raw_q_sent:
        return ['IDEOLOGY'], 'ideology'
    elif 'war' in raw_q_sent or 'blood' in raw_q_sent:
        return ['CAUSE_OF_DEATH'], 'war'
    else:
        return ['O', 'OTHER', 'LOCATION', 'PERSON', 'NUMBER'], 'else'


def get_keywords(sentence):
    return fe.get_word_set_using_spacy(sentence)


def get_named_entities(sentence):
    return fe.get_nes(sentence)


def get_head(sentence):
    return ""
