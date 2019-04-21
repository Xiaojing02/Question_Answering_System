import json
import PickleUtils as pu
import sys
from os import listdir
from os.path import isfile, join
import collections
from Sentence import Sentence
import Preprocessing as pp
import QuestionProcessing as qp
import numpy.matlib
import numpy as np
import scipy
import string
from collections import Counter
from sklearn.metrics import pairwise_distances

# # a Python object (dict):
# x = {
#     "name": "John",
#     "age": 30,
#     "city": "New York"
# }
#
# # convert into JSON:
# y = json.dumps(x)
#
# # the result if a JSON string:
# print(y)
#
#
# folder = sys.argv[1]
# if folder[-1] != "/":
#     folder = folder + "/"
# db = pu.loadData(folder + "database.pickle")  # has some problem: AttributeError:
# # class Sentence has no attribute '__new__'
# # Note: Passing pickles between different versions of
# #  Python can cause trouble, so try to have the same version on both platforms.
# for keys in db:
#     print(keys, '=>', db[keys])


def get_document(question_keywords, doc_db):
    candidate_doc = ["", ""]
    max_len = 0
    max_overlap = 0
    for doc, word_set in doc_db.items():
        cnt = collections.Counter(word_set)
        overlap = 0
        for keyword in question_keywords:
            # overlap = word_set.count(keyword)
            # overlap += cnt[keyword]
            for item in cnt:
                if item in keyword:
                    overlap += cnt[item]
        if overlap > max_overlap:
            max_overlap = overlap
            candidate_doc[0] = doc.document_name
        len_of_intersection = len(set(question_keywords).intersection(word_set))
        # print(cnt.most_common(10))
        # len_of_intersection = len(set(question_keywords).intersection(cnt.most_common(10)))
        if len_of_intersection > max_len:
            max_len = len_of_intersection
            candidate_doc[1] = doc.document_name
    if candidate_doc[0] == candidate_doc[1]:
        candidate_doc.remove(candidate_doc[1])
    # add one more condition: if document name is not in question, remove it
    matched = False
    tmp = []
    for candidate in candidate_doc:
        doc_name = candidate.split(".")[0]
        doc_name = doc_name.translate(str.maketrans('', '', string.punctuation))
        for keyword in question_keywords:
            keyword = keyword.translate(str.maketrans('', '', string.punctuation))
            if keyword in doc_name:
                matched = True
                tmp.append(candidate)
                break
    if matched:
        candidate_doc = tmp
    return candidate_doc


def cosine_similarity(vector1, vector2):
    if scipy.linalg.norm(vector1) == 0 or scipy.linalg.norm(vector2) == 0:
        return -1.0
    score = 1 - scipy.spatial.distance.cosine(vector1, vector2)
    return score


def get_passages(passages, doc_tf_idf, question_tf_idf):
    candidate_passages = {}
    i = 0
    for vector in doc_tf_idf:
        sim_score = cosine_similarity(vector.todense(), question_tf_idf.todense())
        # print("The sim score is: " + str(sim_score))
        candidate_passages[passages[i]] = sim_score
        # if sim_score > 0.08:
        #     candidate_passages[passages[i]] = sim_score
        i += 1
    cnt = Counter(candidate_passages)
    candidates = []
    for candidate_passage in cnt.most_common(6):
        candidates.append(candidate_passage[0])
    return candidates


# def get_passages2(passages, svd_matrix, query_vector):
#     distance_matrix = pairwise_distances(query_vector,
#                                          svd_matrix,
#                                          metric='cosine',
#                                          n_jobs=-1)
#     candidate_passages = {}
#     for i, distance in enumerate(distance_matrix):
#         candidate_passages[passages[i]] = distance
#     cnt = Counter(candidate_passages)
#     candidates = []
#     for candidate_passage in cnt.most_common(6):
#         candidates.append(candidate_passage[0])
#     return candidates


if __name__ == "__main__":
    if len(sys.argv) != 2:
        num = len(sys.argv) - 1
        print(sys.argv[0] + ": got " + str(num)
              + "arguments. Expecting:[corpus_folder]")
        exit()

    path = sys.argv[1]
    if path[-1] != "/":
        path = path + "/"

    # Update_or_not need to be set to True after modifying get_word_set_using_spacy()
    # to re-preprocess the whole database
    document_db = pp.preprocess(path, update_or_not=False)

    questions = ["Who founded Apple Inc.?", "Who supported Apple in creating a new computing platform?",
                "When was Apple Inc. founded?", "When did Apple go public?", "Where is Apple’s headquarters?",
                "Where did Apple open its first retail store?", "When did Abraham Lincoln die?",
                "Where did Thomas Lincoln purchase farms?", "When was the Gettysburg address by Abraham Lincoln?",
                "Who founded UTD?", "When was UTD established?", "Where was Melinda born?",
                "Where is the birth place of Oprah Winfrey?", "Where is the headquarters of AT&T?",
                "Where did AT&T spread to South America?", "When did Warren Buffett buy Berkshire Hathaway's shares?",
                "When did Steve Jobs die?", "Where is the headquarters of Exxon Mobil?",
                "When was ExxonMobile created?", "Where is the headquarters of Amazon.com?",
                 "Who shot Abraham Lincoln?", "Where is UTD located?"]
    answer_documents = ["AppleInc.txt", "AppleInc.txt", "AppleInc.txt", "AppleInc.txt", "AppleInc.txt", "AppleInc.txt",
               "AbrahamLincoln.txt", "AbrahamLincoln.txt", "AbrahamLincoln.txt", "UTD.txt", "UTD.txt",
               "MelindaGates.txt", "OprahWifrey.txt", "AT_T.txt", "AT_T.txt", "Berkshire_Hathaway.txt",
               "LaurenePowellJobs.txt", "ExxonMobil.txt", "ExxonMobil.txt", "Amazon_com.txt",
                        "AbrahamLincoln.txt", "UTD.txt"]
    answers = ["founded by Steve Jobs", "Motorola formed the AIM alliance with the goal of creating", "Apple was founded by Steve Jobs",
               "went public in 1980", "Cupertino, California", "retail stores in Virginia and California",
               "April 15", "leased farms in Kentucky", "November 19, 1863", "Eugene", "creating the University of Texas at Dallas",
               "Melinda Ann French was born", "Mississippi", "multinational conglomerate", "September 2013", "Warren Buffett began buying stock",
<<<<<<< HEAD
               "October 5, 2011", "Irving", "formed in 1999", "Seattle"]

    # Preprocess all the docs in advance(might take a lot of time)
    # Update_or_not need to be set to True after modifying get_all_word_set_using_spacy()
    # to re-preprocess the document
    # p_t_t_dict = pp.preprocess_ti_idf_vector_for_all_files(path, update_or_not=False)

=======
               "October 5, 2011", "Irving", "formed in 1999", "Seattle", "John Wilkes Booth", "Richardson"]
>>>>>>> added noun and verb format of word
    for i, question in enumerate(questions):
        question_keywords = qp.get_keywords(question)
        doc_names = get_document(question_keywords, document_db)
        # print(str(i + 1) + ": " + doc_names[0] + ", " + doc_names[1])
        print(str(i + 1) + ": " + ','.join([doc_name for doc_name in doc_names]))
        print(" Correct answer is: " + answer_documents[i])
        for doc_name in doc_names:

            # Update_or_not need to be set to True after modifying get_all_word_set_using_spacy()
            # to re-preprocess the document
            paragraphs, tfidf, doc_tf_idf = pp.process_ti_idf_vector_for_single_file(path, doc_name, update_or_not=False)

            # If already preprocess all the docs in advance, can just read the tuple from the p_t_t_dict
            # p_t_t_tuple = p_t_t_dict[doc_name]
            # paragraphs, tfidf, doc_tf_idf = p_t_t_tuple[0], p_t_t_tuple[1], p_t_t_tuple[2]

            question_tf_idf = tfidf.transform([question])
            # print(question_tf_idf)
            paragraphs = get_passages(paragraphs, doc_tf_idf, question_tf_idf)
            print(paragraphs)
            for paragraph in paragraphs:
                if answers[i] in paragraph:
                    print("True")


    # for i, question in enumerate(questions):
    #     question_keywords = qp.get_keywords(question)
    #     doc_names = get_document(question_keywords, pp.document_db)
    #     # print(str(i + 1) + ": " + doc_names[0] + ", " + doc_names[1])
    #     print(str(i + 1) + ": " + ','.join([doc_name for doc_name in doc_names]))
    #     print(" Correct answer is: " + answer_documents[i])
    #     for doc_name in doc_names:
    #         file = join(folder, doc_name)
    #         f = open(file, "r")
    #         paragraphs, svd_transformer, svd_matrix = pp.calc_svd_vector(f.read())
    #         query_vector = svd_transformer.transform([question])
    #         # print(question_tf_idf)
    #         paragraphs = get_passages2(paragraphs, svd_matrix, query_vector)
    #         print(paragraphs)
    #         for paragraph in paragraphs:
    #             if answers[i] in paragraph:
    #                 print("True")

    # question = "When did Steve Jobs die?"
    # question_keywords = qp.get_keywords(question)
    # doc_names = get_document(question_keywords, pp.document_db)
    # print("The most matched document is: " + doc_names[0] + ", " + doc_names[1])
    # for doc_name in doc_names:
    #     file = join(folder, doc_name)
    #     f = open(file, "r")
    #     paragraphs, tfidf, doc_tf_idf = pp.calc_ti_idf_vector(f.read())
    #     question_tf_idf = tfidf.transform([question])
    #     print(question_tf_idf)
    #     paragraph = get_passages(paragraphs, doc_tf_idf, question_tf_idf)
    #     print(paragraph)


