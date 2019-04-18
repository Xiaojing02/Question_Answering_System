import json
import PickleUtils as pu
import sys
from os import listdir
from os.path import isfile, join
import collections
from Sentence import Sentence
import Preprocessing as pp
import QuestionProcessing as qp


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

    return candidate_doc


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
        doc_name = get_document(question_keywords, pp.document_db)
        print(str(i + 1) + ": " + doc_name[0] + ", " + doc_name[1])
        print(" Correct answer is: " + answers[i])

    # question = "Who founded Apple Inc.?"
    # question_keywords = qp.get_keywords(question)
    # doc_name = get_document(question_keywords, pp.document_db)
    # print("The most matched document is: " + doc_name)
