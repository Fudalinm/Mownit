import articlesDownloader
import searchEngine

if __name__ == '__main__':
    ######################################################################
    # run if there are no articles befor running please delete data dir  #
    # articlesDownloader.runArticleDownloader()                          #
    ######################################################################

    #######################################################################################################
    # I HAVE NO IDEA HOW TO CACHE THE MATRIX BECAUSE DICT ORDER MIGHT CHANGE AFTER LOADING                #
    # !!PROBABLY!! i can store them because                                                               #
    # 'An OrderedDict is a dictionary subclass that remembers the order in which its contents are added.' #
    #######################################################################################################
    wholeBag, bagForEachFile, matrix, scale_dict, fileVectorDict = searchEngine.initializeBagsOfWords()
    queryBag = searchEngine.takeQuery()
    queryVector = searchEngine.createVectorForQuery(queryBag, wholeBag, scale_dict)
    k = int(input('How many results would you like to see?'))
    results = searchEngine.findResults(queryVector, matrix, fileVectorDict)
    print("HOLY MOLLY! I've got your results!:\n")
    for i in range(1, k + 1):
        print(results[-i][0])

    # TODO: f) Zbadaj jak zachowa się wyszukiwarka po aproksymacji macierzy BoW metodą SVD
    # TODO:    low rank approximation. Dla jakiego rzędu macierzy (bezwzględnego i względem
    # TODO:    rozmiaru macierzy BoW) wyniki są najlepsze/najgorsze, dlaczego?
