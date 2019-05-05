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


def preprocess_ti_idf_vector_for_all_files(path, update_or_not):
    p_t_t_dict = {}
    # Check if the db exixts or not.
    exists = os.path.isfile(saved_ti_idf_path)

    if not exists or update_or_not:
        files = [join(path, f) for f in listdir(path) if isfile(join(path, f))]
        for file in files:
            if file.endswith(".txt"):
                f = open(file, "r")
                data = f.read()
                doc_name = file.split("/")[1]
                print("Calculating ti idf for " + doc_name)
                paragraphs, tfidf, tfs = calc_ti_idf_vector(data)
                p_t_t_dict[doc_name] = (paragraphs, tfidf, tfs)
        file_handler = open(saved_ti_idf_path, 'wb')
        pickle.dump(p_t_t_dict, file_handler)
    else:
        file_handler = open(saved_ti_idf_path, 'rb')
        p_t_t_dict = pickle.load(file_handler)
    return p_t_t_dict


def process_ti_idf_vector_for_single_file(path, doc_name, update_or_not):
    saved_single_doct_ti_idf_path = "Pickle/" + doc_name.split(".")[0] + ".obj"

    # Check if the db exixts or not.
    exists = os.path.isfile(saved_single_doct_ti_idf_path)
    if not exists or update_or_not:
        f = open(join(path, doc_name), "r")
        data = f.read()
        print("Calculating ti idf for " + doc_name)
        doc = Document(doc_name)
        paragraphs, tfidf, tfs = calc_ti_idf_vector(data)
        p_t_t_tuple = (paragraphs, tfidf, tfs)
        file_handler = open(saved_single_doct_ti_idf_path, 'wb')
        pickle.dump(p_t_t_tuple, file_handler)
    else:
        file_handler = open(saved_single_doct_ti_idf_path, 'rb')
        p_t_t_tuple = pickle.load(file_handler)
    return p_t_t_tuple[0], p_t_t_tuple[1], p_t_t_tuple[2] # paragraphs, tfidf, tfs


def get_paragraphs(document):
    paragraphs = document.split("\n\n")
    return paragraphs


def calc_ti_idf_vector(document):
    paragraphs = get_paragraphs(document)
    # print("Num of paragraph: " + str(len(paragraphs)))
    tfidf, tfs = fe.get_tf_idf(paragraphs)
    return paragraphs, tfidf, tfs


def calc_svd_vector(document):
    paragraphs = get_paragraphs(document)
    # print("Num of paragraph: " + str(len(paragraphs)))
    svd_transformer, svd_matrix = fe.get_lsi(paragraphs)
    return paragraphs, svd_transformer, svd_matrix
