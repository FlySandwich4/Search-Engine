from audioop import reverse
from locale import LC_ALL
from queue import PriorityQueue
import json
import Index
import time
global Index_OfIndex 
Index_Of_Index = {}


def changeStringToDict(str):

    doct = {}
    docid_index = str.find('docid')
    tfidf_index = str.find('tfidf')
    fileds_index = str.find('fields')
    tokenfre_index = str.find('Tokenfre')
    lst = str[fileds_index+11:tokenfre_index-5].split("', '")
    WordsInDocid_index = str.find("WordsInDocid")
    positions_index = str.find("Positions")
    last_index = str.find("]}")
    lst_2 = str[positions_index+13:last_index].split(", ")
    for i in range(len(lst_2)):
        lst_2[i] = int(lst_2[i])

    doct["docid"] = int(str[docid_index+8:tfidf_index-3])
    doct["tfidf"] = float(str[tfidf_index+8:fileds_index-3])
    doct["fields"] = lst
    doct["Tokenfre"] = int(str[tokenfre_index+11:WordsInDocid_index-3])
    doct["WordsInDocid"] = int(str[WordsInDocid_index+15:positions_index-3])
    doct["Positions"] = lst_2

    return doct


class QueryClass:

    def __init__(self):
        pass

    #Q means the string of the Query , ex: "apple banana"
    #k means the numbers of webs to return , ex: 3 webs to display
    def DocumentRetrival(self,Q, k):

        #Step 1: breaking Q into words and initialization
            # self.Dict_of_every_Word = {}
            
            # Prior_Queue = PriorityQueue(k)
            # print(self.Dict_of_every_Word)
            List_Seperated_Words_in_Q = Q.lower().split()
            self.Dict_of_every_file = self.build_doc_to_Pos(List_Seperated_Words_in_Q)
            #print(self.Dict_of_every_file)

            doc_to_score = {}


            
            for eachDoc,eachSubDic in self.Dict_of_every_file.items():
                doc_to_score[eachDoc] = 0
                #print(eachDoc, eachSubDic)
                for i,eachWord in enumerate(List_Seperated_Words_in_Q):
                    #print(f"  i: {i}\n  eachWord: {eachWord}\n  eachDoc: {eachDoc}")
                    if eachWord in eachSubDic:         
                        for eachPos in eachSubDic[eachWord][0]:
                            #print(f"    each Position: {eachPos}")
                            
                            doc_to_score[eachDoc] += self.recur_getScore(eachPos,self.Dict_of_every_file,eachDoc,eachWord,List_Seperated_Words_in_Q[i+1:])
                        #print(f"        recursion {eachPos} : {time.time()-recurtime}")    
            
            #print(doc_to_score)
            return doc_to_score


    def build_doc_to_Pos(self,List_Seperated_Words_in_Q):
        Dict_of_every_file = {}

        OpenInvertedList = open("TokenEachLine.txt", 'r')   

        for each in List_Seperated_Words_in_Q:
            #Temp = json.loads(open(f"Lib/{each}.json").read())

            global Index_Of_Index
            #LineNumber = Index_Of_Index[each].first
            StartingByte = Index_Of_Index[each]

            OpenInvertedList.seek(StartingByte) # the byte we start to read
            StringFormat = OpenInvertedList.readline()
            #ListFormat = list(StringFormat)

            StringFormat = StringFormat[1::]
            StringFormat = StringFormat[:-1:]

            LstOfBrackets = StringFormat.split('},')
            for i in range(len(LstOfBrackets)):
                LstOfBrackets[i] += '}'
        

            Temp = []
            for Diction in LstOfBrackets:
                Real_dict = changeStringToDict(Diction)
                Temp.append(Real_dict)
            

            

            counter = 0
            for posting in Temp:
                if posting["docid"] not in Dict_of_every_file:
                    Dict_of_every_file[posting["docid"]] = {}
                Dict_of_every_file[posting["docid"]][each] = (set(posting["Positions"]), posting["tfidf"], posting["WordsInDocid"])
                counter += 1
        #print(Dict_of_every_file)
        return Dict_of_every_file


    #Functionality:
    #       this function will return the score of the certain docid
    #       the score is determined by whether ALL WORDS are in the docid, ex: All A and B and C in the dod
    #       if one of the words doesn't appear, it return 0
    def Count_All_Words(self,i,doc_to_Pos,theDoc,firstWord,secondToEndWords,level=0):
        pass




    #Functionality:
    #       this function input certain position of a word "theword"  and return it's score
    #       when input is ["A","B","C"] and the word is "A", it should return the score of ABC, AB, and A (total score)
    #       
    #Parameters:
    #     --i is the index for positions of each word 
    #     --doc_to_Pos is the dictionary which key is the "docid" and value is "(set(positions), tfidf, words in that doc)"
    #     --List_eachWords is a list of words of seperated words of query excepting the first like["B","C"]
    #     --level is the current words length, like "AB" is level 1 (starting from 0)
    #       which means the score of this level should multiply by 10
    def recur_getScore(self,i,doc_to_Pos,theDoc,theWord,List_eachWords,level=0):
        
        if theWord not in doc_to_Pos[theDoc]:
            return 0
        theword_tup = doc_to_Pos[theDoc][theWord]
        if i not in theword_tup[0]:
            return 0
        elif List_eachWords == []:
            if level == 0:
                return theword_tup[1]
            return ((10**level) * (len(theword_tup[0])/theword_tup[2]))
        elif i in theword_tup[0]:
            if level == 0:
                return theword_tup[1]
            return ((10**level) * (len(theword_tup[0])/theword_tup[2])) + \
                self.recur_getScore(i+1,doc_to_Pos,theDoc,List_eachWords[0],List_eachWords[1:],level+1)


            
    def Count_Score(self,word_List):
        pass

    def seperated_Words(self,s):
        word_list = s.split()
        ReturnS = []
        for lenForSearch in range(2,len(word_list)+1):
            for startIndex in range(len(word_list)):
                try:
                    append_str = ""
                    for eachWord in range(lenForSearch):
                        append_str += word_list[eachWord+startIndex]
                        append_str += " "
                    ReturnS.append(append_str.strip())
                except:
                    break
        return ReturnS

    def seperated_Words2(self, q):
        Score = 0
        lst = q.split()
        for i in lst:
            lst_of_ptr = [0 for i in range(len(lst))]
            #while lst_of_ptr[0] < lst[0]




    def get_All_Common_Doc(self,List_Seperated_Words_in_Q):
        List_Contain_All = []
        for i in json.loads(open(f"Lib/{List_Seperated_Words_in_Q[0]}.json").read()) :
            count = 0
            for each_Words_Except_First in List_Seperated_Words_in_Q[1:]:
                if i["docid"] in [  i["docid"] for i in json.loads(open(f"Lib/{each_Words_Except_First}.json").read())]:
                    count += 1
            if count == len(List_Seperated_Words_in_Q[1:]):
                List_Contain_All.append(i["docid"])
        return List_Contain_All




if __name__ == "__main__":
    # a = myWindows()
    # a.start()

    c = QueryClass()

    

    Index_Of_Index = json.loads(open("IndexOfIndex.json").read())

    start = time.time()

    dict = c.DocumentRetrival("university of the",5)

    f = open("url_index.json","r") 
    lst = json.load(f)

    i = 0
    for each in sorted(dict.keys(), key= lambda x: -dict[x]):
        if i > 4:
            break
        print("================================")
        print(f"    each doc:       {each}")
        print(f"    url:            {lst[each]}")
        print(f"    score of doc:   {dict[each]}")
        print()
        i += 1

    print()
    print("this much of time has been used:", time.time()-start)

    # =======================================================================
    # queryList = ["cristina lopes","machine learning","ACM","master of software engineering"]

    # print()
    # for i in dict:
    #     print("Query For:",i)
    #     lst = DocumentRetrival(i, 5)
    #     with open('url_index.json', 'r') as FA:
    #         LstA = json.load(FA)
    #         for i in lst:
    #             print(LstA[i])
        
    #     print()
    #     print("================================================")
        
