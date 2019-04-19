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
        # if doc.document_name == "LaurenePowellJobs.txt":
            # print(cnt['die'])
            # print(overlap)
            # print(word_set)
        # if doc.document_name == "SteveJobs.txt":
        #     print(overlap)
        #     print(cnt['die'])

    return candidate_doc


def cosine_similarity(vector1, vector2):
    if scipy.linalg.norm(vector1) == 0 or scipy.linalg.norm(vector2) == 0:
        return -1.0
    score = 1 - scipy.spatial.distance.cosine(vector1, vector2)
    return score


def get_passages(passages, doc_tf_idf, question_tf_idf):
    similarity = -1
    candidate_passage = None
    i = 0
    for vector in doc_tf_idf:
        sim_score = cosine_similarity(vector.todense(), question_tf_idf.todense())
        if sim_score > similarity:
            similarity = sim_score
            candidate_passage = passages[i]
        i += 1
    return candidate_passage


if __name__ == "__main__":
    if len(sys.argv) != 2:
        num = len(sys.argv) - 1
        print(sys.argv[0] + ": got " + str(num)
              + "arguments. Expecting:[corpus_folder]")
        exit()

    folder = sys.argv[1]
    if folder[-1] != "/":
        folder = folder + "/"
    files = [join(folder, f) for f in listdir(folder) if isfile(join(folder, f))]
    for file in files:
        print(file)
        if file.endswith(".txt"):
            f = open(file, "r")
            pp.preprocess(f.read(), file)
    questions = ["Who founded Apple Inc.?", "Who supported Apple in creating a new computing platform?",
                "When was Apple Inc. founded?", "When did Apple go public?", "Where is Apple’s headquarters?",
                "Where did Apple open its first retail store?", "When did Abraham Lincoln die?",
                "Where did Thomas Lincoln purchase farms?", "When was the Gettysburg address by Abraham Lincoln?",
                "Who founded UTD?", "When was UTD established?", "Where was Melinda born?",
                "Where is the birth place of Oprah Winfrey?", "Where is the headquarters of AT&T?",
                "Where did AT&T spread to South America?", "When did Warren Buffett buy Berkshire Hathaway's shares?",
                "When did Steve Jobs die?", "Where is the headquarters of Exxon Mobil?",
                "When was ExxonMobile created?", "Where is the headquarters of Amazon.com?"]
    answers = ["AppleInc.txt", "AppleInc.txt", "AppleInc.txt", "AppleInc.txt", "AppleInc.txt", "AppleInc.txt",
               "AbrahamLincoln.txt", "AbrahamLincoln.txt", "AbrahamLincoln.txt", "UTD.txt", "UTD.txt",
               "MelindaGates.txt", "OprahWifrey.txt", "AT_T.txt", "AT_T.txt", "Berkshire_Hathaway.txt",
               "LaurenePowellJobs.txt", "ExxonMobil.txt", "ExxonMobil.txt", "Amazon_com.txt"]
    for i, question in enumerate(questions):
        question_keywords = qp.get_keywords(question)
        doc_names = get_document(question_keywords, pp.document_db)
        print(str(i + 1) + ": " + doc_names[0] + ", " + doc_names[1])
        print(" Correct answer is: " + answers[i])
        for doc_name in doc_names:
            file = join(folder, doc_name)
            f = open(file, "r")
            paragraphs, tfidf, doc_tf_idf = pp.calc_ti_idf_vector(f.read())
            question_tf_idf = tfidf.transform([question])
            # print(question_tf_idf)
            paragraph = get_passages(paragraphs, doc_tf_idf, question_tf_idf)
            print(paragraph)

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


