class Posting:
    def __init__(self,  docid, tfidf, fields):
        #self.token = token # for a specific word
        self.docid = docid # a url
        self.tfidf = tfidf # use freq counts for now

        #fields = []: list contains[ head, p, ...]
        self.fields = [fields]
    
    def add_field(self, Str):
        self.fields.append(Str)

    