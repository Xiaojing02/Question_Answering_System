from nltk.tokenize import RegexpTokenizer
import collections
from nltk.corpus import stopwords


# Get the top N frequent word in the document(exclude the stop word)
f = open("WikipediaArticles/NYC.txt", "r")
tokenizer = RegexpTokenizer(r'\w+')
stopWords = set(stopwords.words('english'))
ws = []
for line in f:
    tokens = tokenizer.tokenize(line)
    for token in tokens:
        token = token.lower()
        if token not in stopWords:
            ws.append(token)
print(ws)
cnt = collections.Counter(ws)
print(cnt.most_common(5))