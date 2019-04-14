from nltk.corpus import wordnet


# Given a word, get its synsets and its corresponding lemmas.
# Future improvement, take POS into account to filter out some synset
syns = wordnet.synsets("go")

print(syns)

set = set()
for s in syns:
    lemmasOfs = s.lemmas()
    # print(lemmasOfs)
    for le in lemmasOfs:
        print(le.name())
