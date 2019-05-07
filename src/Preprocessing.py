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
import pickle

saved_db_path = 'Pickle/db.obj'
saved_ti_idf_path = 'Pickle/ti_idf.obj'
saved_ner_path = 'Pickle/named_entities.obj'


# use spaCy processing pipeline to process original documents
def preprocess(path, update_or_not):
    document_db = {}
    # Check if the db exixts or not.
    exists = os.path.isfile(saved_db_path)

    if not exists or update_or_not:
        files = [join(path, f) for f in listdir(path) if isfile(join(path, f))]
        for file in files:
            if file.endswith(".txt"):
                f = open(file, "r")
                data = f.read()
                doc_name = file.split("/")[1]
                print(doc_name)
                word_set = fe.get_word_set_using_spacy(data)
                doc = Document(doc_name)
                document_db[doc] = word_set
        file_handler = open(saved_db_path, 'wb')
        pickle.dump(document_db, file_handler)
    else:
        file_handler = open(saved_db_path, 'rb')
        document_db = pickle.load(file_handler)
    return document_db


def preprocess_ner_for_all_files(path, update_or_not):
    p_t_t_dict = {}
    # Check if the db exixts or not.
    exists = os.path.isfile(saved_ner_path)

    if not exists or update_or_not:
        files = [join(path, f) for f in listdir(path) if isfile(join(path, f))]
        for file in files:
            if file.endswith(".txt"):
                f = open(file, "r")
                data = f.read()
                doc_name = file.split("/")[1]
                print("Extracting ner for " + doc_name)
                paragraphs = get_paragraphs(data)
                nes_lists = []
                for paragraph in paragraphs:
                    nes_lists.append([nes_list for nes_list in pp.get_named_entities(paragraph)])
                p_t_t_dict[doc_name] = (paragraphs, nes_lists)
        file_handler = open(saved_ner_path, 'wb')
        pickle.dump(p_t_t_dict, file_handler)
    else:
        file_handler = open(saved_ner_path, 'rb')
        p_t_t_dict = pickle.load(file_handler)
    return p_t_t_dict


def process_ner_for_single_file(path, doc_name, update_or_not):
    saved_single_doct_ner_path = "Pickle/" + doc_name.split(".")[0] + ".obj"

    # Check if the db exixts or not.
    exists = os.path.isfile(saved_single_doct_ner_path)
    if not exists or update_or_not:
        f = open(join(path, doc_name), "r")
        data = f.read()
        print("Extracting ner for " + doc_name)
        paragraphs = get_paragraphs(data)
        nes_lists = []
        for paragraph in paragraphs:
            nes_lists.append([nes_list for nes_list in get_named_entities(paragraph)])
        p_t_t_tuple = (paragraphs, nes_lists)
        file_handler = open(saved_single_doct_ner_path, 'wb')
        pickle.dump(p_t_t_tuple, file_handler)
    else:
        file_handler = open(saved_single_doct_ner_path, 'rb')
        p_t_t_tuple = pickle.load(file_handler)
    return p_t_t_tuple[0], p_t_t_tuple[1]  # paragraphs, nes_lists


def get_ti_idf_vector(paths):
    documents = []
    for path in paths:
        f = open(path, "r")
        data = f.read()
        documents.append(data)
    print("Calculating ti idf")
    tfidf, tfs = calc_ti_idf_vector(documents)
    files = []
    for path in paths:
        if path.endswith(".txt"):
            doc_name = path.split("/")[1]
            files.append(doc_name)
    return files, documents, tfidf, tfs  # document_name_list, documents, tfidf, tfs


def get_paragraphs(document):
    paragraphs = document.split("\n\n")
    return paragraphs


def calc_ti_idf_vector(documents):
    # print("Num of paragraph: " + str(len(paragraphs)))
    tfidf, tfs = fe.get_tf_idf(documents)
    return tfidf, tfs


def lower_tokens(words):
    return [word.lower() for word in words]


def get_named_entities(passage):
    return fe.get_nes(passage)


def get_number_of_right_nes():
    return 0


def get_number_of_question_keywords():
    return 0


def get_longest_exact_sequence():
    return 0


def get_passage_feature_vectors():
    return 0
