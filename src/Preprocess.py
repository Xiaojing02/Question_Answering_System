from wiki_Reader import Sentence
import os
import collections
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import nltk
import spacy
import pickle


nlp = spacy.load("en_core_web_sm")

# lemmatizer = WordNetLemmatizer()
# tokens = set(nltk.word_tokenize("When was Apple Inc. founded?"))
# stopWords = set(stopwords.words('english'))
# tokens = tokens - stopWords
# print(tokens)
# for token in tokens:
#     print(lemmatizer.lemmatize(token, pos="n"))
#     token = lemmatizer.lemmatize(token, pos="n")
#     print(wordnet.synsets(token))
# tagged = nltk.pos_tag(tokens)
# print(tagged)

def load_data(path):
    database = {}
    for fileName in os.listdir(path):
        if fileName.endswith(".txt"):
            f = open(path + "/" + fileName, "r", encoding = "ISO-8859-1")
            for line in f:
                if len(line) > 1:
                    sentences = line.split(".")
                    for sentence in sentences:
                        word_set = get_word_set_by_Spacy_lemma(sentence)
                        sen = Sentence(sentence, word_set, fileName)
                        put_word_set_in_map(word_set, database, sen)
    return database


def get_sentence_features(sentence):
    keyword_set = set()
    stopWords = set(stopwords.words('english'))
    tokens = set(nltk.word_tokenize(sentence))
    tokens = tokens - stopWords
    for token in tokens:
        synset = wordnet.synsets(token)
        for synonym in synset[:3]:
            lemmas_of_synonym = synonym.lemmas()
            for lemmas in lemmas_of_synonym:
                word_set.add(lemmas.name())
    return word_set

def get_word_set_by_Spacy(sentence):
    stopWords = set(stopwords.words('english'))
    word_set = set()
    doc = nlp(sentence)
    for X in doc.ents:
        if X.text not in stopWords:
            word_set.add(X.text + "|" + X.label_)
            # print(X.text + "|" + X.label_)
    return word_set

def get_word_set_by_Spacy_lemma(sentence):
    stopWords = set(stopwords.words('english'))
    word_set = set()
    doc = nlp(sentence)
    for token in doc:
        if token.lemma_ not in stopWords:
            word_set.add(token.lemma_ + "|" + token.tag_)
        # print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
        #       token.shape_, token.is_alpha, token.is_stop)
    return word_set

def put_word_set_in_map(word_set, database, sen):
    database[sen] = word_set


# Need more work to calculate the score and return top N candidates.
def get_intersection(question_sentence, db):
    question_sentence_set = get_word_set(question_sentence)
    max = 0
    answer_sen = None
    for sen, word_set in db.items():
        len_of_intersection = len(question_sentence_set.intersection(word_set))
        if  len_of_intersection > max:
            max = len_of_intersection
            answer_sen = sen
    return answer_sen

def get_candidates(question_sentence, db):
    question_sentence_set = get_word_set_by_Spacy_lemma(question_sentence)
    sim_dict = {}
    for sen, word_set in db.items():
        len_of_intersection = len(question_sentence_set.intersection(word_set))
        sim_dict[sen] = len_of_intersection
    cnt = collections.Counter(sim_dict)
    for sen in cnt.most_common(10):
        print(sen[1], sen[0].sentence)
    # print(cnt.most_common(3))


if __name__ == "__main__":

    question = "When was Apple Inc. founded?"
    path = "./WikipediaArticles"
    saved_db_path = 'db.obj'

    exists = os.path.isfile(saved_db_path)
    if exists:
        filehandler = open(saved_db_path, 'rb')
        db = pickle.load(filehandler)
    else:
        db = load_data(path)
        filehandler = open(saved_db_path, 'wb')
        pickle.dump(db, filehandler)

    # Obtains the candidates from database
    # Current problem: 考虑的词越多越得不到正确的句子, 当前进度: 把所有出现词的synset取intersection (search among all the documents)
    # Possible improvement: Get keywords for each document and the question, and only search for limited documents.
    get_candidates(question, db)
    # answer_sentence = get_intersection(question, db)
    # print(answer_sentence.sentence)
    # print(answer_sentence.document_name)

    #Analyze all the candidates to get the correct answer