__author__ = 'Vikas'

import json
import math
import collections
import sys


def main():

    if len(sys.argv) == 5:
        indexFile = sys.argv[1]
        queryFile = sys.argv[2]
        maxDocResults = sys.argv[3]
        outputFile = sys.argv[4]
        Error = True
    else:
        Error = False
        print "Four arguments expected"

    if Error:
        loadFiles(indexFile, queryFile, maxDocResults, outputFile)

def loadFiles(indexFile, queryFile, maxDocResults, outputFile):

    ## Dictionary to store bm25 scores.
    ## Key -> DocID, value -> bm25 score
    bm25 = collections.defaultdict(int)

    indexFile = open(indexFile, "r")

    ## Load the two dictionaries from the file.
    ds = json.load(indexFile)
    invertedIndex = ds[0]
    docTokenCount = ds[1]

    indexFile.close()

    ## Load queries into list
    with open(queryFile, "r") as file:
        queries = file.readlines()

    ## Total number of documents
    totalDoc = len(docTokenCount)
    totalTokens = sum(docTokenCount.values())
    averageLength = totalTokens/float(totalDoc)

    print "Total number of documents ->" , totalDoc
    print "Total number of tokens ->" , totalTokens
    print "Average length of each document ->" , averageLength

    queryID = 0

    outputfile = open(outputFile, 'w')

    for eachQuery in queries:
        queryID += 1

        ## Clear the dictionary for each new query
        bm25.clear()

        ## Split the queries into each terms
        terms = eachQuery.split()

        ## Calculating the bm25 score for each document in which the current term occurs
        for term in terms:
            termfreq = invertedIndex.get(term)

            for docID in termfreq:
                tokenCount = docTokenCount.get(docID)
                queryCount = eachQuery.count(term)
                bm25score = calculatebm25(docID, termfreq, totalDoc, averageLength, tokenCount, queryCount)
                bm25[docID] += bm25score

        ## Sort the bm25 scores and store into a list
        sortedBM25 = sorted([(v , k) for k, v in bm25.iteritems()], reverse=True)

        ## Output results in the given format
        displayOutput(sortedBM25[0:int(maxDocResults)], outputfile, queryID)

    outputfile.close()
    print "Results written in ->" , outputFile



def calculatebm25(docID, termfreq, totalDoc, averageLength, tokenCount, queryCount):
    k1 = 1.2
    k2 = 100
    b = 0.75
    N = totalDoc
    qfi = queryCount

    ## No relevance Information available.
    r = 0
    R = 0

    ## Total number of documents in which term occurs.
    ni = len(termfreq)

    ## Calculating K from the formula
    K = k1 * ((1 - b) + (b * tokenCount/averageLength))

    ## Number of times term occured in the DocID
    fi = termfreq.get(docID)

    b1 = float(((r + 0.5)/(R - r + 0.5)) * ((N - ni - R + r + 0.5)/(ni - r + 0.5)))
    b2 = float(((k1 + 1) * fi)/(K + fi))
    b3 = float(((k2 + 1) * qfi)/(k2 + qfi))

    ## bm25 score formula.
    bm25score  = math.log(b1) * b2 * b3

    return  bm25score

def displayOutput(sortedBM25, outputFile, queryID):
    r = 0
    system_name = "Vikas Shriyan"

    headings = "Query ID".center(10) +\
                "Q0".center(10) +\
                "Document ID".rjust(14) +\
                "Rank".rjust(8) +\
                "BM25 Score".rjust(15) +\
                "system_name".center(26)
    outputFile.write(headings + "\n")
    for score, docID in sortedBM25:
        r += 1

        ## Output Format
        line = str(queryID).center(10) +\
               " Q0 ".center(10) +\
                str(docID).rjust(10) +\
                str(r).rjust(10) +\
                str(score).rjust(20) +\
                system_name.center(20)

        outputFile.write( line + "\n")


if __name__ == '__main__':
    main()
