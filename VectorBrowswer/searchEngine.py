import os
import collections
import re
import json
import numpy as np
from math import log
import operator

bagOfWords = []  # LATER IT WILL BE A DICT
bagForEachFile = {}


def initializeBagsOfWords():
    global bagOfWords
    global bagForEachFile
    loadBagOfWordsFromFile()
    if bagOfWords == {}:
        os.makedirs('cache')
        createBagOfWords()
        x, y, z = CreateVectorForEachFile(bagForEachFile, bagOfWords)
    x, y, z = loadDictsAndMatrix()
    return bagOfWords, bagForEachFile, x, y, z


def loadDictsAndMatrix():
    global bagOfWords
    global bagForEachFile
    x = collections.OrderedDict()
    y = collections.OrderedDict()
    m = np.zeros(shape=(len(bagOfWords), len(bagForEachFile)))
    try:
        with open('cache/PRESCALER_DICT', 'r', encoding='utf8') as fp:
            x = json.load(fp)
        with open('cache/FILE_VECTOR_DICT', 'r', encoding='utf8') as fp:
            y = json.load(fp)
        m = np.load('cache/MATRIX.npy')
    except FileNotFoundError:
        print("...")
        return m, x, y
    return m, x, y


def loadBagOfWordsFromFile():
    global bagOfWords
    global bagForEachFile
    try:
        with open('cache/WHOLE_BAG', 'r', encoding='utf8') as fp:
            bagOfWords = json.load(fp)
        with open('cache/BAG_FOR_EACH_FILE', 'r', encoding='utf8') as fp:
            bagForEachFile = json.load(fp)
    except FileNotFoundError:
        bagForEachFile = collections.OrderedDict()
        bagOfWords = collections.OrderedDict()
        print("Could not find cache directory")
    bagForEachFile = collections.OrderedDict(bagForEachFile)
    bagOfWords = collections.OrderedDict(bagOfWords)
    return bagOfWords, bagForEachFile


def createBagOfWords():
    lineList = []
    global bagOfWords
    global bagForEachFile
    # vectors = codecs.open('data/vectors', 'w', 'utf-8')
    for filename in os.listdir("data/"):
        if filename == 'data': continue
        # print(filename)
        if os.path.isfile("data/" + filename):
            # otwieramy i zbieramy kazde ze slow
            f = open("data/" + filename, 'r', encoding="utf8")
            text = f.read().split('\n')
            lineList.extend(text)
            # tmp = [collections.Counter(re.findall(r'\w+', txt)) for txt in text]
            # if len(text) > 2:
            #     print(text)
            #     print(tmp)
            # bagForEachFile[filename] = dict([collections.Counter(re.findall(r'\w+', txt)) for txt in text][0])
            bagForEachFile[filename] = dict(
                sum([collections.Counter(re.findall(r'\w+', txt)) for txt in text], collections.Counter()))
    print("Loaded all text from files. \n Creating bags.")
    bagOfWords = [collections.Counter(re.findall(r'\w+', txt)) for txt in lineList]
    bagOfWords = sum(bagOfWords, collections.Counter())
    # wen need to have strict order of words
    bagOfWords = collections.OrderedDict(bagOfWords)
    bagForEachFile = collections.OrderedDict(bagForEachFile)

    print("Creating cache for bags.")
    # storing as json
    with open('cache/WHOLE_BAG', 'w', encoding='utf8') as fp:
        json.dump(bagOfWords, fp)

    with open('cache/BAG_FOR_EACH_FILE', 'w', encoding='utf8') as fp:
        json.dump(bagForEachFile, fp)


def CreateVectorForEachFile(orderedBagForEachFile, orderedWholeBag):
    print("Creating vectors for articles and matrix")
    # we need to have dict in stric order
    prescalerDict = collections.OrderedDict()
    fileVectorDict = collections.OrderedDict()
    m = np.zeros(shape=(len(orderedWholeBag), len(orderedBagForEachFile)))
    wordIndex = 0
    for word in orderedWholeBag.keys():
        #######################################################
        # IDF(w) = w*log N/nw                                 #
        # N -   numberOfDocuments                             #
        # nw - liczba dokumentow w ktorych wystepuje to slowo #
        #######################################################
        N = len(orderedBagForEachFile)
        nw = 0
        for documentName in orderedBagForEachFile.keys():
            # jezeli to slowo jest w slowniku
            if word in orderedBagForEachFile[documentName]:
                nw += 1
        if log(N / nw) == 0: print(N, nw)
        prescalerDict[word] = (log(N / nw), wordIndex)
        fileIndex = 0
        for documentName in orderedBagForEachFile.keys():
            if wordIndex == 1:
                fileVectorDict[documentName] = fileIndex
            inThisDocument = 0
            if word in orderedBagForEachFile[documentName]:
                inThisDocument = orderedBagForEachFile[documentName][word]
            m[wordIndex, fileIndex] = inThisDocument * log(N / nw)
            fileIndex += 1
        wordIndex += 1
    print("Caching vectors and matrix.")
    # we need to store them in file
    with open('cache/PRESCALER_DICT', 'w', encoding='utf8') as fp:
        json.dump(prescalerDict, fp)
    with open('cache/FILE_VECTOR_DICT', 'w', encoding='utf8') as fp:
        json.dump(fileVectorDict, fp)
    np.save('cache/MATRIX', m)

    print("Everything cached!")

    return m, prescalerDict, fileVectorDict


def takeQuery():
    query = input("Write your query :-) : ")
    bagForQuery = dict(collections.Counter(re.findall(r'\w+', query)))
    return bagForQuery


def createVectorForQuery(queryBag, orderedWholeBag, scaleDict):
    print("Creating query vector")
    v = np.zeros(shape=(len(orderedWholeBag), 1))
    for word in orderedWholeBag.keys():
        scale, wordIndex = scaleDict[word]
        if word in queryBag.keys():
            v[wordIndex, 0] = scale * queryBag[word]
        else:
            v[wordIndex, 0] = 0
    return v


def findResults(queryVecotr, matrix, fileVectorDict):
    print("Searching for best matches!")
    transposedQueryVector = np.transpose(queryVecotr)
    results = []
    queryVectorNorm = np.linalg.norm(queryVecotr)
    documentsNumber = len(fileVectorDict)

    for documentName in fileVectorDict.keys():
        column = fileVectorDict[documentName]
        cosinusMetric = np.matmul(transposedQueryVector, matrix[:, column]) / \
                        queryVectorNorm * np.linalg.norm(matrix[:, column])
        results.append((documentName, cosinusMetric))

    # results = sorted(results, key=results.get)
    return sorted(results, key=lambda res: res[1])
