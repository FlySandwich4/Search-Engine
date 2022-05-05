import math

def findAllUrl(fileName):
    pass

#CountOfT: count of T in This Doc
#NumOfWords: The number of words in this document
#Documents: The total number of documents
#TotalOccur: The number of documents that contain T
def countTFIDF(self, CountOfT, NumOfWords, Documents, TotalOccur): 
    return (CountOfT/NumOfWords)*math.log(Documents/TotalOccur)


    



