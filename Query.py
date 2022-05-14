from audioop import reverse
from queue import PriorityQueue
import json
import Index


def DocumentRetrival(Q, k):
    
    L = []
    R = PriorityQueue(k)

    Q = Q.lower().split()
    hash_table = json.loads(open("AllWords0.json").read())
    
    for term in Q:
        l = hash_table[term]
        L.append((term, l))
    
    for a in range(1, 1989):

        docScore = 0
        for invertedList in L:
            for x in invertedList[1]:
                if x["docid"] == a:
                    
                    #print(x["tfidf"])
                    #print(Index.countTFIDF(Q.count(invertedList[0]), len(Q), 1988, len(invertedList[1])))
                    docScore += (Index.countQueryTFIDF(Q.count(invertedList[0]), len(Q), 1988, len(invertedList[1])) * x["tfidf"])     
        if R.qsize() < k:
            #print("hah")
            R.put([docScore, a])
        else:
            #print("hehe")
            check = R.get()
            if docScore > check[0]:
                R.put([docScore, a])
            else:
                R.put(check)
    print(R.queue)
    
    docIDList = []
    while(not R.empty()):
        docIDList.append(R.get())

    docIDList = [x[1] for x in sorted(docIDList, key = lambda x: -x[0])]

    return docIDList
                




if __name__ == "__main__":
    # a = myWindows()
    # a.start()
    query = "machine learning"
    query = "University of California"
    print()
    lst = DocumentRetrival(query, 5)
    with open('url_index.json', 'r') as FA:
        LstA = json.load(FA)
        for i in lst:
            print(LstA[i])
