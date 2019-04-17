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

import spacy


nlp = spacy.load('en_core_web_sm')
doc = nlp(u'Apple is looking at buying U.K. startup for $1 billion')

for token in doc:
    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
            token.shape_, token.is_alpha, token.is_stop)

#
# import spacy
# from spacy.pipeline import EntityRecognizer
# from spacy import displacy
# from collections import Counter
# nlp = spacy.load("en_core_web_sm")
# # doc = nlp('supported Apple in creating a new computing platform?')
# # print([(X.text, X.label_) for X in doc.ents])
# doc2 = nlp('When was the Gettysburg address by Abraham Lincoln')
# print(set(doc2.ents))
# print([(X.text, X.label_) for X in doc2.ents])

# import nltk
# from nltk import word_tokenize
# from nltk.util import ngrams
# from collections import Counter
#
# text = "I need to write a program in NLTK that breaks a corpus (a large collection of txt files) into unigrams, bigrams, trigrams, fourgrams and fivegrams. I need to write a program in NLTK that breaks a corpus"
# token = nltk.word_tokenize(text)
# unigrams = ngrams(token,1)
# bigrams = ngrams(token,2)
# trigrams = ngrams(token,3)
# fourgrams = ngrams(token,4)
# fivegrams = ngrams(token,5)
#
# print(Counter(trigrams))

