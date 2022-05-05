import math
from pathlib import Path
# import re
import os
import json


def findAllUrl(path):
    # entries = Path(path)
    # for entry in entries.iterdir():
    #     print(entry)
    #     if re.match(r"[0-9a-zA-Z_]*" ,str(entry)):
    #         print("  this is path+entry {}".format(str(path) + str(entry)))
    #         findAllUrl(path+entry)
    #     elif re.match(r"[0-9a-zA-Z_]*\.json",str(entry)):
    #         print("  Match Jason")

    j_files = []
    # add all paths of files end with ".json" into j_files 
    for r, d, files in os.walk(path):
        for f in files:
            if f.endswith('.json'):
                j_files.append(os.path.join(r, f))
    # open all files 
    for j in j_files:
        info = open(j, "r").read()


#CountOfT: count of T in This Doc
#NumOfWords: The number of words in this document
#Documents: The total number of documents
#TotalOccur: The number of documents that contain T
def countTFIDF(self, CountOfT, NumOfWords, Documents, TotalOccur): 
    return (CountOfT/NumOfWords)*math.log(Documents/TotalOccur)


if __name__ =="__main__":
    findAllUrl('ANALYST/')

    



