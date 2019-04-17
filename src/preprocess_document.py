from nltk.tokenize import RegexpTokenizer
import collections
from nltk.corpus import stopwords
import spacy

nlp = spacy.load("en_core_web_sm")

# Get the top N frequent word in the document(exclude the stop word)
f = open("WikipediaArticles/NYC.txt", "r")
tokenizer = RegexpTokenizer(r'\w+')
stopWords = set(stopwords.words('english'))
ws = []
word_set = []
for line in f:
    doc = nlp(line)
    for X in doc.ents:
        if X.text not in stopWords:
            word_set.append(X.text + "|" + X.label_)
    tokens = tokenizer.tokenize(line)
    for token in tokens:
        token = token.lower()
        if token not in stopWords:
            ws.append(token)

# print(ws)
cnt = collections.Counter(ws)
print(cnt.most_common(5))
cnt2 = collections.Counter(word_set)

print(cnt2.most_common(10))