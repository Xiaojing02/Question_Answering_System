import pickle


def storeData(db, filename):
    dbfile = open(filename, 'wb')

    pickle.dump(db, dbfile, protocol=2)
    dbfile.close()


def loadData(filename):
    dbfile = open(filename, 'rb')
    db = pickle.load(dbfile)
    dbfile.close()
    return db


# # path to pickle folder
# pickle_dir = sys.path[1] + "/pickle/"
#
#
# # sentences setter and getter
# def set_sentences(sentences):
#     with open(pickle_dir + "sentences.pickle", 'wb') as output:
#         pickle.dump(sentences, output)
#
#
# def get_sentences():
#     with open(pickle_dir + "sentences.pickle", 'rb') as input:
#         sentences = pickle.load(input)
#     return sentences
#
#
# # words setter and getter
# def set_words(words):
#     with open(pickle_dir + "words.pickle", 'wb') as output:
#         pickle.dump(words, output)
#
#
# def get_words():
#     with open(pickle_dir + "words.pickle", 'rb') as input:
#         words = pickle.load(input)
#     return words
#
#
# # pos_tags_all setter and getter
# def set_pos_tags(pos_tags):
#     with open(pickle_dir + "pos_tags.pickle", 'wb') as output:
#         pickle.dump(pos_tags, output)
#
#
# def get_pos_tags():
#     with open(pickle_dir + "pos_tags.pickle", 'rb') as input:
#         pos_tags = pickle.load(input)
#     return pos_tags
