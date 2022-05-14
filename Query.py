from audioop import reverse
from queue import PriorityQueue
import json
import Index


class QueryClass:

    def __init__(self):
        pass

    #Q means the string of the Query , ex: "apple banana"
    #k means the numbers of webs to return , ex: 3 webs to display
    def DocumentRetrival(self,Q, k):
        
        #Step 1: breaking Q into words and initialization
            List_Seperated_Words_in_Q = Q.lower().split()
            Prior_Queue = PriorityQueue(k)
        
        
        #Step 2: Iterate every word in List_Seperated_Words_in_Q and execute some judgments:
        #   Judgement 1:  A n B n C
        #       1): Find intersection
            List_Contain_All = []
 
            for i in json.loads(open(f"Lib/{List_Seperated_Words_in_Q[0]}.json").read()) :
                count = 0
                for each_Words_Except_First in List_Seperated_Words_in_Q[1:]:
                    if i["docid"] in [  i["docid"] for i in json.loads(open(f"Lib/{each_Words_Except_First}.json").read())]:
                        count += 1
                if count == len(List_Seperated_Words_in_Q[1:]):
                    List_Contain_All.append(i["docid"])
            
            print(List_Contain_All)
                    



        #   Jdugement 2:  A U B U C
            


            
            return []



    #============================= FROMER CODES
        #59393 is the total nums of the docs
        # for a in range(1, 55394):

        #     docScore = 0
        #     for invertedList in L:
        #         for x in invertedList[1]:
        #             if x["docid"] == a:
                        
        #                 #print(x["tfidf"])
        #                 #print(Index.countTFIDF(Q.count(invertedList[0]), len(Q), 1988, len(invertedList[1])))
        #                 docScore += (Index.countQueryTFIDF(Q.count(invertedList[0]), len(Q), 55393, len(invertedList[1])) * x["tfidf"]) 

            # if R.qsize() < k:
            #     #print("hah")
            #     R.put([docScore, a])
            # else:
            #     #print("hehe")
            #     check = R.get()
            #     if docScore > check[0]:
            #         R.put([docScore, a])
            #     else:
            #         R.put(check)
        #print(R.queue)

        # docIDList = []
        # while(not R.empty()):
        #     docIDList.append(R.get())
        # docIDList = [x[1] for x in sorted(docIDList, key = lambda x: -x[0])]
        #return docIDList
    #============================= FROMER CODES ENDS HERE


                




if __name__ == "__main__":
    # a = myWindows()
    # a.start()


    c = QueryClass()
    c.DocumentRetrival("lab study engine",20)

    # =======================================================================
    # queryList = ["cristina lopes","machine learning","ACM","master of software engineering"]

    # print()
    # for i in queryList:
    #     print("Query For:",i)
    #     lst = DocumentRetrival(i, 5)
    #     with open('url_index.json', 'r') as FA:
    #         LstA = json.load(FA)
    #         for i in lst:
    #             print(LstA[i])
        
    #     print()
    #     print("================================================")
        
