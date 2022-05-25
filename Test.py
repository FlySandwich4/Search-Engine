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

if __name__ == "__main__":
    std = "{'docid': 338, 'tfidf': 0.011013049261506142, 'fields': ['p', 'h2', 'title', 'head'], 'Tokenfre': 5, 'WordsInDocid': 218, 'Positions': [328561, 328810, 200021619, 400011761, 500011761]}"
    D = changeStringToDict(std)
    print(D)


