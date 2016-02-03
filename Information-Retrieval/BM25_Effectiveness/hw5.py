__author__ = 'Vikas'

import sys
import collections
import math



relevantDocs = {} ## Dictionary to store Key -> Query IDs, value -> Doc IDs

resultsDict = {} ##  Dictionary to store Key -> Query IDs , Value -> OrderedDictionary
                 ##  OrderedDictionary Key -> DocID , Value -> BM25 Score.

def main():

    if len(sys.argv) == 3:
        cacm = sys.argv[1]
        results = sys.argv[2]
        Error = True
    else:
        Error = False
        print "Two arguments expected"

    if Error:
        loadFiles(cacm,results)

def loadFiles(cacm, results):

    ## Store the cacm relevant query ids and doc ids
    file = open(cacm, "r")
    for line in file :
        word = line.split()
        id = word[0]
        docId = word[2]
        if id not in relevantDocs.keys():
            relevantDocs[id] = []
        relevantDocs[id].append(docId)


    ## Store the query id, scores and doc ids
    results = open(results, "r")
    for line in results:
        word = line.split()
        id = word[0]
        if id == "1":
            id = "12"
        elif id == "2":
            id = "13"
        else:
            id = "19"
        docID = "CACM-"+word[2]
        score = word[4]

        if id not in resultsDict.keys():
           resultsDict[id] = collections.OrderedDict()

        resultsDict[id][docID] = score


    ## Initializing output Dictionary for storing values of precision, recall, relevance level, doc ID
    ## and NDCG for that particular query ID.
    outputDict = {}
    A = 0
    MAP = 0.0
    pk = {} ## Dictionary to store p@k values where query ID is the key and value is the precision value at k=20
    for qID, value in resultsDict.iteritems():
        A = len(relevantDocs.get(qID)) ## Number of relevant docs
        B = 0 ## Number of retrieved documents
        relevantDocsFound = 0
        rank = 0
        AvP = 0.0 ## Average Precision value
        prevDCG = 0.0 ## Discounted Cumulative gain
        prevIDCG = 0.0 ## Ideal Discounted Cumulative gain
        temp = collections.OrderedDict() ## Temp dictionary to store doc Ids as key and list of precision, recall, etc. as value
        for did, score in value.iteritems():
            rank += 1 ## Next document
            B += 1
            values = []

            ## Append the score
            values.append(score)

            ## Update the relevance level for each doc ID and append to the list of values
            if did in relevantDocs.get(qID):
                relevanceLevel = 1
            else:
                relevanceLevel = 0
            values.append(relevanceLevel)

            ## Update relevant Docs found
            if relevanceLevel == 1:
               relevantDocsFound += 1

            ## Calculate Precision
            precision = float(relevantDocsFound)/float(B)
            if(relevanceLevel == 1):
                AvP += precision

            ## Calculate P@K where K = 20
            if(rank == 20):
                pk[qID] = precision
            values.append(precision)

            ## Calculate RECALL
            recall = float(relevantDocsFound)/float(A)
            values.append(recall)

            ## Calculate NDCG
            if(rank == 1):
                dcg = relevanceLevel
            else:
                dcg = float(relevanceLevel)/math.log(rank, 2)

            if(rank == 1):
                idcg= 1
            elif(rank <= A):
                idcg = 1.0/(math.log(rank, 2))
            else:
                idcg = 0.0

            dcg += prevDCG
            idcg += prevIDCG

            ndcg = dcg/idcg
            values.append(ndcg)

            ## Add the values for that particular DOC ID
            temp[did] = values

            prevIDCG = idcg
            prevDCG = dcg

        ## Calculate Average Precision
        AvP = AvP/relevantDocsFound
        MAP += AvP

        ## Add the DOC ID for the particular query ID
        outputDict[qID] = temp

    ## Calculate MAP
    MAP = MAP/3


    ## Printing out the values
    outputDict = collections.OrderedDict(sorted(outputDict.items(), key=lambda t: t[0]))
    for queryID in outputDict.keys():
        print "***********************************************", "QUERY ID ", queryID , "******************************************************"
        print  "Rank".center(10) +\
                "Document ID".center(10) +\
                "Document Score".rjust(19) +\
                "Relevance Level".rjust(22) +\
                "Precision".rjust(15) +\
                "Recall".rjust(19) +\
                "NDCG".rjust(14) + "\n"
        rank = 0
        for v1, v2 in outputDict.get(queryID).iteritems():
            rank += 1
            print str(rank).center(10) +\
                  str(v1).center(10) +\
                  str(v2[0]).rjust(20) +\
                  str(v2[1]).rjust(15) +\
                  str(v2[2]).rjust(20) +\
                  str(v2[3]).rjust(20) +\
                  str(v2[4]).rjust(15)


    print "MAP -> " , MAP , "P@K -> " , pk

if __name__ == '__main__':
    main()
