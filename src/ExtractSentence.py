from BM25 import BM25Okapi
import string


corpus = [
    "Hello there good man!",
    "It is quite windy in London",
    "How is the weather today?"
]

tokenized_corpus = [doc.split(" ") for doc in corpus]

bm25 = BM25Okapi(tokenized_corpus)

query = "windy London"
tokenized_query = query.split(" ")

doc_scores = bm25.get_scores(tokenized_query)
bm25.get_top_n(tokenized_query, corpus, n=1)

candidate_passages = get_passages(answer_types, paragraphs, doc_ner)

sentences = []
for passage in candidate_passages:
    sen = passage.split('. ')
    for s in sen:
        sentences.append(s)
for sentence in sentences:
    word_set = fe.get_word_set_using_spacy(sentence)
    bm25 = BM25Okapi(word_set)