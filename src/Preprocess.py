from wiki_Reader import Sentence
import os
import collections
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import nltk

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
            f = open(path + "/" + fileName, "r")
            for line in f:
                if len(line) > 1:
                    sentences = line.split(".")
                    for sentence in sentences:
                        word_set = get_word_set(sentence)
                        sen = Sentence(sentence, word_set, fileName)
                        put_word_set_in_map(word_set, database, sen)
    return database


def get_word_set(sentence):
    word_set = set()
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
    question_sentence_set = get_word_set(question_sentence)
    sim_dict = {}
    for sen, word_set in db.items():
        len_of_intersection = len(question_sentence_set.intersection(word_set))
        sim_dict[sen] = len_of_intersection
    cnt = collections.Counter(sim_dict)
    for sen in cnt.most_common(10):
        print(sen[1], sen[0].sentence)
    # print(cnt.most_common(3))


if __name__ == "__main__":

    question = "go public apple?"
    path = "./WikipediaArticles"
    # print(get_word_set("When did Apple go public?"))
    db = load_data(path)

    # Obtains the candidates from database
    # Current problem: 考虑的词越多越得不到正确的句子, 当前进度: 把所有出现词的synset取intersection (search among all the documents)
    # Possible improvement: Get keywords for each document and the question, and only search for limited documents.
    get_candidates(question, db)
    answer_sentence = get_intersection(question, db)
    print(answer_sentence.sentence)
    print(answer_sentence.document_name)

    #Analyze all the candidates to get the correct answer