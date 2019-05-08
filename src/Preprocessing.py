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
saved_sent_to_doc_map_path = 'Pickle/sent_to_doc_map.obj'
saved_sent_to_realsent_map_path = 'Pickle/sent_to_para_maps.obj'

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


def preprocess_passage(passage, doc_name, passage_num):
    saved_passage_path = "Pickle/" + doc_name.split(".")[0] + str(passage_num) + ".obj"

    # Check if the db exixts or not.
    exists = os.path.isfile(saved_passage_path)
    if not exists or update_or_not:
        sen = passage.split('. ')
        sen_word_set = []
        for s in sen:
            word_set = fe.get_word_set_using_spacy(sentence)
            sen_word_set.append((s, word_set))
        file_handler = open(saved_passage_path, 'wb')
        pickle.dump(sen_word_set, file_handler)
    else:
        file_handler = open(saved_passage_path, 'rb')
        sen_word_set = pickle.load(file_handler)
    return sen_word_set  # paragraphs, nes_lists


def get_ti_idf_vector(paths):
    exists = os.path.isfile(saved_ti_idf_path)
    if not exists:
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
        p_t_t_tuple = (files, documents, tfidf, tfs)
        file_handler = open(saved_ti_idf_path, 'wb')
        pickle.dump(p_t_t_tuple, file_handler)
    else:
        file_handler = open(saved_ti_idf_path, 'rb')
        p_t_t_tuple = pickle.load(file_handler)
    return p_t_t_tuple[0], p_t_t_tuple[1], p_t_t_tuple[2], p_t_t_tuple[3]  # document_name_list, documents, tfidf, tfs


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
    return fe.get_nes_with_spacy(passage)


def get_named_entities_with_spacy(passage):
    fe.get_nes_with_spacy(passage)


def preprocess_get_sent_to_doc_and_realsent_map(path):
    sent_to_doc_map = {}
    sent_to_realsent_map = {}
    # Check if the db exixts or not.
    exists1 = os.path.isfile(saved_sent_to_doc_map_path)
    exists2 = os.path.isfile(saved_sent_to_realsent_map_path)

    if not exists1 or not exists2:
        files = [join(path, f) for f in listdir(path) if isfile(join(path, f))]
        for file in files:
            if file.endswith(".txt"):
                f = open(file, "r")
                data = f.read()
                doc_name = file.split("/")[1]
                paragraphs = get_paragraphs(data)
                for paragraph in paragraphs:
                    sentences = paragraph.split('. ')
                    for sentence in sentences:
                        word_set = fe.get_word_set_using_spacy(sentence)
                        key = str(word_set)
                        sent_to_doc_map[key] = doc_name
                        sent_to_realsent_map[key] = sentence
        file_handler = open(saved_sent_to_doc_map_path, 'wb')
        pickle.dump(sent_to_doc_map, file_handler)
    else:
        file_handler = open(saved_sent_to_doc_map_path, 'rb')
        file_handler2 = open(saved_sent_to_realsent_map_path, 'rb')
        sent_to_doc_map = pickle.load(file_handler)
        sent_to_realsent_map = pickle.load(file_handler2)
    return sent_to_doc_map, sent_to_realsent_map

