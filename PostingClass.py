class Posting:
    def __init__(self, docid, tfidf, fields):
        self.docid = docid
        self.tfidf = tfidf # use freq counts for now
        self.fields = fields