__author__ = 'Vikas'

import sys
import json
import re

docTokenCount = {}          ## Dictionary to store token count number for each doc ID.
                            ## Key -> Document ID, Value -> Number of tokens in each doc.

docTokenCollection = {}     ## Dictionary to store words for each doc ID.
                            ## Key -> Document ID, Value -> list of words

invertedIndex = {}          ## Dictionary for Inverted Index
                            ## Key -> word, Value -> term freq, {docID : tf } for key

data = []                   ## List with Inverted Index and Number of tokens for each document

def main():
    if len(sys.argv) == 3:
        inputFile = sys.argv[1]
        outputFile = sys.argv[2]
        Error = True
    else:
        Error = False
        print "Two arguments expected"


    if Error:
        buildInvertedIndex(inputFile, outputFile)

def buildInvertedIndex(inputFile, outputFile):

    ## Read the corpus file and create a list of tokenized document
    ## Each new document starts "#" character
    with open(inputFile,"r") as file:
        docText = file.read()
        docList = re.split('\# ',docText)
        numberOfDoc = len(docList)


    # First line of the document is empty
    docList.pop(0)

    for eachLine in docList:
        words = re.findall(r"\w+" , eachLine)


        ## First Word is the Document ID
        docID = words[0]



        ## Building the document collection.
        ## First element is the Document ID, hence remove it
        ## Key -> docID , value -> list of words
        words.pop(0)

        ## Removing tokens that contain only the digits 0-9
        for each in words:
            if each.isdigit():
                words = filter(lambda i: not str.isdigit(i), words)

        ## Leave out the first word, i.e., document ID
        tokenCount = len(words)

        ## Store key -> Doc ID, value -> number of tokens in doc
        docTokenCount[docID] = tokenCount

        docTokenCollection[docID] = words

    ## Building Inverted Index
    for docID, docWords in docTokenCollection.iteritems():
        for eachWord in docWords:
            temp = {}
            if eachWord in invertedIndex:
                if docID in invertedIndex.get(eachWord):
                    ## Increase the word count
                    invertedIndex[eachWord][docID] += 1
                else:
                    ## Doc ID occuring for the first time, set count to 1
                    invertedIndex[eachWord][docID] = 1
            else:
                ## Word occuring for the first time
                temp[docID] = 1
                invertedIndex[eachWord] = temp


    opFile  = open(outputFile , "w")

    ## Write the inverted index and number of tokens in each document into ds.
    data = [invertedIndex , docTokenCount]
    json.dump(data, opFile, indent = 4)

    opFile.close()

    print "Results written in this file ->" , outputFile


if __name__ == '__main__':
    main()



