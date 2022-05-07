#/==========================================\
#|This hw is done by a group with 4 members:|
#|   Name        ;NetID      ;StudentID     |
#|   Yue Wu      ;wu57       ;16762451      |
#|   Hao Ying    ;hying5     ;49709238      |
#|   Sicheng Liu ;sichel14   ;59658402      |
#|   Xin Zhou    ;xinz36     ;83222896      |
#\==========================================/

import re
import sys



def READ(file): # O(N)
    Tokens = [] # O(1)


    a = file.rstrip('\n') #O(1) since much smaller than A, since one line has multiple words
    elements = re.split("\W+", a) #O(N) have to allocate every words in the file into a list, so linear
    for j in elements: #O(N) already go through all words in the file, O(N)
        j = j.replace("_", "") # exclude words containing _ # O(N) although with a very small factor like 0.01*N
        if not j.isdigit(): # exclude complete numbers like 123, 456, but keep sth like 1st, 2nd
            # to exclude the situation that 're, 't... However, if the 'xx is longer than 2, it probably means sth
            # so in that situation, I would keep that
            # O(N) since every words has to be checked
            if len(j) > 2: # O(N) since nearly every words has to be checked
                j = j.lower() # O(N) since nearly every words has to be lowered
                Tokens.append(j) # O(N) since nearly every words has to be appended

    return Tokens

def Count(Tokens): #O(NlogN)
    Tokens.sort() # O(NlogN)
    #print(Tokens)
    counter = 0 # O(1)
    last = "" # O(1)
    D = {} #O(1)
    while counter < len(Tokens): # O(N) since only go through the elements for once
        if Tokens[counter] != last: #O(N) since every time have to check if it's the last word
            last = Tokens[counter] #O(N)
            D[last] = 0 # O(N)
        D[last] += 1 #O(N) since every time have to add one
        counter +=1 #O(N) since every time have to add one
    return D

def Printer(D): #O(NlogN)
    for i in sorted(D, key = lambda x : -D[x]): # since used sorted, O(NlogN)
        print(i, '-' ,D[i]) #O(N)

if __name__ == '__main__': # O(NlogN)
    file_name = "/Users/liusicheng/Desktop/ics121/Book1"
    #file_name = input("input your text file: ")
    #file_name = sys.argv[1]
    Tokens = READ(open(file_name, 'r'))
    D = Count(Tokens)
    Printer(D)
    #utils.response.Response