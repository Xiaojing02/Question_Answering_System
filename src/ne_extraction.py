import spacy
from spacy import displacy
from collections import Counter



# Testing using the sample questions, ne is unique.
nlp = spacy.load("en_core_web_sm")
# doc = nlp('supported Apple in creating a new computing platform?')
# print([(X.text, X.label_) for X in doc.ents])
doc2 = nlp('When was the Gettysburg address by Abraham Lincoln')
print(set(doc2.ents))
print([(X.text, X.label_) for X in doc2.ents])

