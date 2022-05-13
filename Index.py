
#/==========================================\
#|This hw is done by a group with 4 members:|
#|   Name        ;NetID      ;StudentID     |
#|   Yue Wu      ;wu57       ;16762451      |
#|   Hao Ying    ;hying5     ;49709238      |
#|   Sicheng Liu ;sichel14   ;59658402      |
#|   Xin Zhou    ;xinz36     ;83222896      |
#\==========================================/

from asyncore import write
import math
from operator import iand
from re import A
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
global jsonNums
jsonNums = 0
import sys
import time

print("success import")


def findAllUrl(path):
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
    return list(j_files)
        

#return : {token: posting}
def BuildSmallIndex(DocList,DocIndex):
    #print("build function's toal {}".format(total_doc))
    Hash_Table = {}
    
    for eachFile in DocList:
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


        for token, tokenPostings in Hash_Table.items():
            TotalOccurOfThisToken = len(tokenPostings)
            for eachPosting in tokenPostings:
                eachPosting.tfidf = countTFIDF(eachPosting.Tokenfre, eachPosting.WordsInDocid, total_doc, TotalOccurOfThisToken)

    return Hash_Table


        
def BuildIndex(D):
    global jsonNums
    Hash_Table = {}
    n = 0
    B = []
    
    #Breaking Large D into small B List
    theI = 0
    while D != []:
        for i in range(500):
            try:
                B.append(D.pop())
            except:
                break

        Hash_Table = BuildSmallIndex(B,n)

        with open("AllWords{theI}.json".format(theI = theI), "w+") as F:
            print("Building Json File:", "AllWords{theI}.json".format(theI = theI))
            #for token in sorted(Hash_Table.keys()):
           #     json_obj = json.dumps({token: [i.__dict__ for i in Hash_Table[token]]}, indent=4)
                

            json_obj = json.dumps({token: [i.__dict__ for i in Hash_Table[token]] for token in sorted(Hash_Table.keys())}, indent=4 )
            F.write(json_obj)

        theI += 1
        Hash_Table = {}
        B = []
        n += 500
        jsonNums += 1
        


def Merge(file_A, file_B):
    print(f"Merging {file_A} and {file_B}")
    #initialize
    fA = open(file_A)
    fB = open(file_B)
    Table_A = json.load(fA)
    Table_B = json.load(fB)
    KeysA = sorted(Table_A.keys())
    KeysB = sorted(Table_B.keys())
    indexA = 0
    indexB = 0

    """
    apple, banana,lsc, sb, zx
    [p1, p2, p3] -< p4

    apple, lsc, yh
    [p4, p5, p6]

    total Json file -> parameter 1
    each file json (in order) -> parameter 2

    put into merge: only change total json file
    """

    while not (indexA == len(KeysA) and indexB == len(KeysB)):
        try:
            if KeysA[indexA] < KeysB[indexB]:
                indexA += 1
            
            elif KeysA[indexA] == KeysB[indexB]:
                Table_A[KeysA[indexA]] += Table_B[KeysB[indexB]]
                indexA += 1
                indexB += 1

            elif KeysB[indexB] < KeysA[indexA]:
                Table_A[KeysB[indexB]] = Table_B[KeysB[indexB]]
                indexB += 1
        except:
            if indexA == len(KeysA):
                Table_A[KeysB[indexB]] = Table_B[KeysB[indexB]]
                indexB += 1
            if indexB == len(KeysB):
                break

    fA.close()
    fA = open(file_A, "w+")
                          
    json_obj = json.dumps({token: [i for i in Table_A[token]] for token in sorted(Table_A.keys())}, indent=4)
    fA.write(json_obj)

    fA.close()

    
    fB.close()


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
    BuildIndex(findAllUrl('DEV/'))

    print("\nStart Merging\n===========================================")
    for i in range(1,jsonNums):
        Merge("AllWords0.json", "AllWords{i}.json".format(i=i))
        os.remove("AllWords{i}.json".format(i=i))
    



