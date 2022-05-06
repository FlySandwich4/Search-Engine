class Posting:
    def __init__(self,  docid, tfidf, fields, Tokenfre, WordsInDocid):
        #self.token = token # for a specific word
        self.docid = docid # a url
        self.tfidf = tfidf # use freq counts for now

        #fields = []: list contains[ head, p, ...]
        self.fields = [fields]

        #the word frequency appear in this doc
        self.Tokenfre = Tokenfre

        #the total words in this docid
        self.WordsInDocid = WordsInDocid
    
    def add_field(self, Str):
        self.fields.append(Str)

    def __str__(self):
        return "---This posting docid: {d} \n   field: {f}\n   tfidf: {t}".format(d=self.docid, f=self.fields, t=self.tfidf)