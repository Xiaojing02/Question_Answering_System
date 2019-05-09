import sys
from os import listdir
from os.path import isfile, join
import Preprocessing as pp
import QuestionProcessing as qp
import scipy
from collections import Counter
import FeatureExtraction as fe
from rank_bm25 import BM25Okapi
import json


def cosine_similarity(vector1, vector2):
    if scipy.linalg.norm(vector1) == 0 or scipy.linalg.norm(vector2) == 0:
        return -1.0
    score = 1 - scipy.spatial.distance.cosine(vector1, vector2)
    return score


def get_document(doc_names, documents, doc_tf_idf, question_tf_idf):
    candidate_documents = {}
    i = 0
    for vector in doc_tf_idf:
        sim_score = cosine_similarity(vector.todense(), question_tf_idf.todense())
        candidate_documents[(doc_names[i], documents[i])] = sim_score
        i += 1
    cnt = Counter(candidate_documents)
    candidates_doc_names = []
    candidate_passages = []
    for candidate_document in cnt.most_common(6):
        candidates_doc_names.append(candidate_document[0][0])
        candidate_passages.append(candidate_document[0][1])
    return candidates_doc_names, candidate_passages


def get_passages(answer_types, passages, doc_ner):
    candidate_passages = []
    i = 0
    for passage in passages:
        doc_nes = set([ne[1] for ne in doc_ner[i]])
        overlap = answer_types.intersection(doc_nes)
        if overlap:
            candidate_passages.append(passage)
        i += 1
    return candidate_passages


if __name__ == "__main__":
    if len(sys.argv) != 3:
        num = len(sys.argv) - 1
        print(sys.argv[0] + ": got " + str(num)
              + "arguments. Expecting:[corpus_folder]")
        exit()

    path = sys.argv[1]
    if path[-1] != "/":
        path = path + "/"
    files = [join(path, f) for f in listdir(path) if isfile(join(path, f)) and join(path, f).endswith(".txt")]

    #task3
    input_path = sys.argv[2]
    # Process at the beginning of task3
    sent_to_doc_map, sent_to_realsent_map = pp.preprocess_get_sent_to_doc_and_realsent_map(path)
    questions = []
    with open(input_path, "r") as file:
        for line in file:
            line = line.replace(u'\ufeff', '')
            questions.append(line.rstrip('\n'))
    print("Finished load map")
    answer_list = []
    for i, question in enumerate(questions):
        # use tf-idf to get candidate documents and the results are ordered by their rankings
        doc_names, documents, tfidf, doc_tf_idf = pp.get_ti_idf_vector(files)
        question_tf_idf = tfidf.transform([question])
        candidate_documents, documents = get_document(doc_names, documents, doc_tf_idf, question_tf_idf)
        print(str(i + 1) + ". Candidate documents: ")
        print(candidate_documents)

        # Question Processing: get query keywords and answer types
        question_keywords = qp.get_keywords(question)
        # print(question_keywords)
        answer_types = set([ne[1] for ne in qp.get_named_entities(question)])
        question_type, answer_type = qp.identify_question_type(qp.extract_wh_word(question.split()),
                                                               question.split())
        # print(question_type)
        answer_types = answer_types.union(set(question_type))
        # print(answer_types)

        # Passage Retrieval and Sentence Selection
        # First use Answer types filter out passages without relevant entities
        # Then use features to rank passages
        candidate_sentences = []
        sentences = []
        for doc_name in candidate_documents:
            paragraphs, doc_ner = pp.process_ner_for_single_file(path, doc_name, update_or_not=False)
            candidate_passages = get_passages(answer_types, paragraphs, doc_ner)
            for passage in candidate_passages:
                sen = passage.split('. ')
                for s in sen:
                    sentences.append(s)
        corpus = []
        for sentence in sentences:
            word_set = fe.get_word_set_using_spacy(sentence)
            corpus.append(word_set)
        if len(corpus) != 0:
            bm25 = BM25Okapi(corpus)
            question_word_set = fe.get_word_set_using_spacy(question)
            doc_scores = bm25.get_scores(question_word_set)
            candidate_sentences = bm25.get_top_n(question_word_set, corpus, n=3)
            answer_dict = {}
            answer_dict["Question"] = question
            answer_dict["answers"] = {}
            answer_dict["sentences"] = {}
            answer_dict["documents"] = {}
            j = 1
            for candidate_sentence in candidate_sentences:
                key = str(candidate_sentence)
                sen_ner = [ne for ne in qp.get_named_entities(sent_to_realsent_map[key])]
                # print(sen_ner)
                answers = []
                for ne in sen_ner:
                    # print(ne[1])
                    if ne[1] in question_type:
                        answers.append(ne[0])
                doc_name = sent_to_doc_map[key]
                sentence = sent_to_realsent_map[key]

                answer_dict["answers"][str(j)] = ', '.join(answers)
                answer_dict["sentences"][str(j)] = sentence
                answer_dict["documents"][str(j)] = doc_name
                j += 1
            print(answer_dict)
        else:
            print("Answer is not found.")
            answer_dict = {}

        answer_list.append(answer_dict)

    with open('output.json', 'w') as outfile:
        json.dump(answer_list, outfile)



