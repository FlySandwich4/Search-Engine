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
from urllib.parse import urlparse
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
global F_lst
F_lst = ['empty']
import sys
import time
global this_time
this_time = 0
print("success import")


def findAllUrl(path):
    j_files = set()
    # add all paths of files end with ".json" into j_files 
    #url_set = set()
    for r, d, files in os.walk(path):
        for f in files:
            if f.endswith('.json'):
                #if not parsed.netloc + parsed.path in url_set:
                j_files.add(os.path.join(r, f))

    #global total_doc
    # open all files 
    #total_doc = len(j_files)
    #print("This is total {}".format(total_doc))
    File_lst = list(j_files)

    
    return File_lst
        
class buildIndex:
    def __init__(self):
        self.p_last_index = 0
        self.h3_last_index = 100000000
        self.h2_last_index = 200000000
        self.h1_last_index = 300000000
        self.title_last_index = 400000000
        self.head_last_index = 500000000
    #return : {token: posting}
    
    def BuildSmallIndex(self, DocList,DocIndex):
        #print("build function's toal {}".format(total_doc))
        global F_lst
        global this_time
        global total_doc
        Hash_Table = {}        
        for eachFile in DocList:            
            data = json.loads(open(eachFile).read())
            url = data['url']
            parsed = urlparse(url)
            new_url = parsed.netloc + parsed.path
            if new_url not in F_lst:
                DocIndex += 1
                F_lst.append(new_url)
                total_doc += 1
                this_time += 1          
                sp = BeautifulSoup(data["content"], "lxml")
                              
                # A dictionary containing all tokens' corresponding positions
                regions = ['p', 'h3', 'h2', 'h1', 'title', 'head']
                total_text = ""
                for r in regions:
                    for TextInEachRegion in sp.find_all(r): 
                        total_text += TextInEachRegion.text
                        total_text += " "
                
                Dict = Tokenizer.READ(total_text) 

                Len = sum(len(i) for i in Dict.values()) # length of 

                # p: paragraph  h#: small titles 
                
                for regionInText in regions:

                    for TextInEachRegion in sp.find_all(regionInText):
                        tokens_position = Tokenizer.READ(TextInEachRegion.text)
                        d = Tokenizer.Count(tokens_position) 
                        
                        for k in d:
                            lst = tokens_position[k]
                            if k in Hash_Table:
                                if not Hash_Table[k][-1].docid == DocIndex:
                                    Hash_Table[k].append(Posting(DocIndex, 0, regionInText, d[k], Len))
                                else:
                                    if regionInText not in Hash_Table[k][-1].fields:
                                        Hash_Table[k][-1].add_field(regionInText)
                                    Hash_Table[k][-1].Tokenfre += d[k]
                            else:
                                Hash_Table[k] = []
                                Hash_Table[k].append(Posting(DocIndex, 0, regionInText, d[k], Len))

                            if regionInText == 'p':
                                lst = [i + self.p_last_index for i in lst]
                                self.p_last_index = self.p_last_index + len(lst) + 2
                            elif regionInText == 'h3':
                                lst = [i + self.h3_last_index for i in lst]
                                self.h3_last_index = self.h3_last_index + len(lst) + 2
                            elif regionInText == 'h2':
                                lst = [i + self.h2_last_index for i in lst]
                                self.h2_last_index = self.h2_last_index + len(lst) + 2
                            elif regionInText == 'h1':
                                lst = [i + self.h1_last_index for i in lst]
                                self.h1_last_index = self.h1_last_index + len(lst) + 2
                            elif regionInText == 'title':
                                lst = [i + self.title_last_index for i in lst]
                                self.title_last_index = self.title_last_index + len(lst) + 2
                            elif regionInText == 'head':
                                lst = [i + self.head_last_index for i in lst]
                                self.head_last_index = self.head_last_index + len(lst) + 2
                            Hash_Table[k][-1].Positions += lst


        for token, tokenPostings in Hash_Table.items():
            TotalOccurOfThisToken = len(tokenPostings)
            for eachPosting in tokenPostings:
                eachPosting.tfidf = countTFIDF(eachPosting.Tokenfre, eachPosting.WordsInDocid, total_doc, TotalOccurOfThisToken)

        return Hash_Table

            
    def BuildIndex(self,D):
        global jsonNums
        global this_time
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

            Hash_Table = self.BuildSmallIndex(B,n)

            with open("AllWords{theI}.json".format(theI = theI), "w+") as F:
                print("Building Json File:", "AllWords{theI}.json".format(theI = theI))
                #for token in sorted(Hash_Table.keys()):
            #     json_obj = json.dumps({token: [i.__dict__ for i in Hash_Table[token]]}, indent=4)
                    

                json_obj = json.dumps({token: [i.__dict__ for i in Hash_Table[token]] for token in sorted(Hash_Table.keys())}, indent=4 )
                F.write(json_obj)

            theI += 1
            Hash_Table = {}
            B = []
            n += this_time
            this_time = 0
            #n += 500
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

    return (CountOfT/NumOfWords)*(math.log(Documents/TotalOccur,10))

# def countTF(CountOfT, NumOfWords):
#     return (CountOfT/NumOfWords)
def countQueryTFIDF(CountOfT, NumOfWords, Documents, TotalOccur):
    return (1+math.log(CountOfT/NumOfWords, 10))*(math.log(Documents/TotalOccur,10))

if __name__ =="__main__":
    BI = buildIndex()
    BI.BuildIndex(findAllUrl('ANALYST/'))
    with open('url_index.json', 'w+') as F1:
        json_obj = json.dumps(F_lst)
        F1.write(json_obj)

    print("\nStart Merging\n===========================================")
    for i in range(1,jsonNums):
        Merge("AllWords0.json", "AllWords{i}.json".format(i=i))
        os.remove("AllWords{i}.json".format(i=i))

    

    hash_table = json.loads(open("AllWords0.json").read())
    try:
        os.makedirs("Lib")
    except:
        pass
    for token in hash_table:
        with open("Lib/"+token + '.json', 'w+') as File:
            json_obj = json.dumps(hash_table[token],indent=4)
            File.write(json_obj)

    os.remove("AllWords0.json")
    



