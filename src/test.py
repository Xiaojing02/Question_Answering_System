# import gensim
# from gensim.parsing.preprocessing import preprocess_documents
#
# # documents = []
# # f = open('AppleInc.txt', 'r')
# # documents = preprocess_documents(f)
# # for line in f:
# #     documents.append(line)
# #
# # print(documents)
# #
# #
# # model = gensim.models.Word2Vec(
# #         documents,
# #         size=150,
# #         window=10,
# #         min_count=2,
# #         workers=10)
# # model.train(documents, total_examples=len(documents), epochs=10)
#
# gensim.corpora.wikicorpus.WikiCorpus(fname, processes=None, lemmatize=True, dictionary=None, filter_namespaces=('0', ), tokenizer_func=<function tokenize>, article_min_tokens=50, token_min_len=2, token_max_len=15, lower=True, filter_articles=None)
#
# print(model.wv.most_similar("design"))


