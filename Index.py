
#/==========================================\
#|This hw is done by a group with 4 members:|
#|   Name        ;NetID      ;StudentID     |
#|   Yue Wu      ;wu57       ;16762451      |
#|   Hao Ying    ;hying5     ;49709238      |
#|   Sicheng Liu ;sichel14   ;59658402      |
#|   Xin Zhou    ;xinz36     ;83222896      |
#\==========================================/

import math
import urllib.request
from pathlib import Path
# import re
import os
import json
from pydoc import Doc
from bs4 import BeautifulSoup
import urllib
import Tokenizer
from PostingClass import Posting
global total_doc
total_doc = 0
import sys

print("success import")


def findAllUrl(path):
    # entries = Path(path)
    # for entry in entries.iterdir():
    #     print(entry)
    #     if re.match(r"[0-9a-zA-Z_]*" ,str(entry)):
    #         print("  this is path+entry {}".format(str(path) + str(entry)))
    #         findAllUrl(path+entry)
    #     elif re.match(r"[0-9a-zA-Z_]*\.json",str(entry)):
    #         print("  Match Jason")

    j_files = set()
    # add all paths of files end with ".json" into j_files 
    for r, d, files in os.walk(path):
        for f in files:
            if f.endswith('.json'):
                j_files.add(os.path.join(r, f))
    global total_doc
    # open all files 
    total_doc = len(j_files)
    print("This is total {}".format(total_doc))
    return j_files
        

#return : {token: posting}
def BuildIndex(DocSet):
    print("build function's toal {}".format(total_doc))
    Hash_Table = {}
    DocIndex = 0
    for eachFile in DocSet:
        DocIndex += 1
        data = json.loads(open(eachFile).read())

        sp = BeautifulSoup(data["content"], "lxml")

        WholeTextInEachFile = sp.get_text()
        # A dictionary containing all tokens' corresponding positions
        Dict = Tokenizer.READ(WholeTextInEachFile) 

        Len = sum(len(i) for i in Dict.values()) # length of 

        # p: paragraph  h#: small titles 
        regions = ['p', 'h3', 'h2', 'h1', 'title', 'head']
        for regionInText in regions:

            for TextInEachRegion in sp.find_all(regionInText):
                d = Tokenizer.Count(Tokenizer.READ(TextInEachRegion.text)) 

                for k in d:
                    if k in Hash_Table:
                        if not Hash_Table[k][-1].docid == DocIndex:
                            Hash_Table[k].append(Posting(DocIndex, 0, regionInText, d[k], Len))
                            if regionInText == 'p' and k in Dict:
                                Hash_Table[k][-1].Positions = Dict[k]
                        else:
                            Hash_Table[k][-1].add_field(regionInText)
                            Hash_Table[k][-1].Tokenfre += d[k]
                    else:
                        Hash_Table[k] = []
                        Hash_Table[k].append(Posting(DocIndex, 0, regionInText, d[k], Len))
                        if regionInText == 'p' and k in Dict:
                            Hash_Table[k][-1].Positions = Dict[k]

                #i
                #FileDic {token  : d[1] dic[token][1].append(i)}
        
        # for token, tokenPostings in Hash_Table.items():
        #     TotalOccurOfThisToken = len(tokenPostings)
        #     for eachPosting in tokenPostings:
        #         eachPosting.tfidf = countTFIDF(eachPosting.Tokenfre, eachPosting.WordsInDocid, total_doc, TotalOccurOfThisToken)

        # for k,v in Hash_Table.items():
        #     print("={}".format(k))
        #     for each in v:
        #         print(countTF(each.Tokenfre, each.WordsInDocid))
        #         #print("    Word fre in total", each.Tokenfre)
        #         #print("    Total Words", each.WordsInDocid)
        #         print("    DocID",each.docid)
        

    #print("total_doc", total_doc)
    #print("total unique words", len(Hash_Table))
    #print("The size of the disk", sys.getsizeof(Hash_Table)/1024, "kb (",sys.getsizeof(Hash_Table),"bytes )")
    for token in sorted(Hash_Table.keys()):
        i = 0
        print(token)
        for pos in Hash_Table[token]:
            print("    Postings{i}: {d}, {p}".format(t=token, i=i, d = pos.docid, p = pos.Positions))
            i += 1
        print("-------------------------------------------------------------")




#CountOfT: count of T in This Doc
#NumOfWords: The number of words in this document
#Documents: The total number of documents
#TotalOccur: The number of documents that contain T
def countTFIDF(CountOfT, NumOfWords, Documents, TotalOccur): 
    #print(Documents)
    #print("^ doc  v total")
    #print(TotalOccur)

    return (CountOfT/NumOfWords)*(math.log(Documents/TotalOccur,2))

def countTF(CountOfT, NumOfWords):
    return (CountOfT/NumOfWords)


if __name__ =="__main__":
    BuildIndex(findAllUrl('ANALYST/'))

    



