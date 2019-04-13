from wiki_Reader import Sentence
import os


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
    return set(sentence.split())


def put_word_set_in_map(word_set, database, sen):
    database[sen] = word_set


# Need more work to calculate the score and return top N candidates.
def get_intersection(question_sentence, dict):
    question_sentence_set = get_word_set(question_sentence)
    max = 0
    answer_sen = None
    for sen, word_set in dict.items():
        len_of_intersection = len(question_sentence_set.intersection(word_set))
        if  len_of_intersection > max:
            max = len_of_intersection
            answer_sen = sen
    return answer_sen


if __name__ == "__main__":

    question = "Who supported Apple in creating a new computing platform?"
    path = "./WikipediaArticles"

    db = load_data(path)

    answer_sentence = get_intersection(question, db)
    print(answer_sentence.sentence)
    print(answer_sentence.document_name)

    #Analyze the candidates