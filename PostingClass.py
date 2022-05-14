#/==========================================\
#|This hw is done by a group with 4 members:|
#|   Name        ;NetID      ;StudentID     |
#|   Yue Wu      ;wu57       ;16762451      |
#|   Hao Ying    ;hying5     ;49709238      |
#|   Sicheng Liu ;sichel14   ;59658402      |
#|   Xin Zhou    ;xinz36     ;83222896      |
#\==========================================/

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
        self.Positions = []
    
    def add_field(self, Str):
        if str not in self.fields:
            self.fields.append(Str)

    def __str__(self):
        return "---This posting docid: {d} \n   field: {f}\n   tfidf: {t}".format(d=self.docid, f=self.fields, t=self.tfidf)