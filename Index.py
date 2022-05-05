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
import PostingClass



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
    # open all files 
    return j_files
        

#return : {token: posting}
def BuildIndex(DocSet):
    Hash_Table = {}
    DocIndex = 0
    for eachFile in DocSet:
        DocIndex += 1
        data = json.loads(open(eachFile).read())
        
        sp = BeautifulSoup(data["content"], "lxml")
        #f = sp.get_text()
        lst = ['p', 'h3', 'h2', 'h1', 'title', 'head']
        #FileDic= {}
        for i in lst:
            for j in sp.find_all(i):
                d = Tokenizer.Count(Tokenizer.READ(j.text)) #d[1]
                print(i, d)
                for k in d:
                    if k in Hash_Table:
                        Hash_Table[k].append(Posting(DocIndex, d[k], i))
                    else:
                        Hash_Table[k] = []
                        Hash_Table[k].append(Posting(DocIndex, d[k], i))

                #i
                #FileDic {token  : d[1] dic[token][1].append(i)}


        
        #Tokenizer.Printer(d)
                #print("here executed")
        #(data["content"])
        #



#CountOfT: count of T in This Doc
#NumOfWords: The number of words in this document
#Documents: The total number of documents
#TotalOccur: The number of documents that contain T
def countTFIDF(self, CountOfT, NumOfWords, Documents, TotalOccur): 
    return (CountOfT/NumOfWords)*math.log(Documents/TotalOccur)


if __name__ =="__main__":
    BuildIndex(findAllUrl('ANALYST/'))

    



