class Sentence:
    # More features to add, e.g. type, relations
    def __init__(self, sentence, word_set, pos_tags, document_name):
        self.sentence = sentence
        self.word_set = word_set
        self.pos_tags = pos_tags
        self.document_name = document_name
