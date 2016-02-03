__author__ = 'Vikas'

import sys
import glob
import json

termsNeg = {}                   ## Dictionary to store terms from Negative Data in Test directory
                                ## Key -> term, Value -> Term Frequency

termsPos = {}                   ## Dictionary to store terms from Positive Data in Test directory
                                ## Key -> term, Value -> Term Frequency

model_data = []                 ## List to dump the json data into the file.

vocab = {}

def main():

    if len(sys.argv) == 3:
        textcat = sys.argv[1]
        model = sys.argv[2]
        Error = True
    else:
        Error = False
        print "Two arguments expected"

    if Error:
        loadFiles(textcat,model)

def loadFiles(textcat, model):
    ## Load the negative directory files
    train_neg_path = textcat+'/train/neg/*.txt'
    train_neg_files = glob.glob(train_neg_path)
    for file in train_neg_files:
        file = open(file, "r")
        for line in file:
            word = line.split()
            for w in word:
                if w not in termsNeg:
                    termsNeg[w] = 1
                else:
                    termsNeg[w] += 1
                if w not in vocab:
                    vocab[w] = 1
                else:
                    vocab[w] += 1

    ## Load the positive directory files
    train_pos_path = textcat+'/train/pos/*.txt'
    train_pos_files = glob.glob(train_pos_path)
    for file in train_pos_files:
        file = open(file, "r")
        for line in file:
            word = line.split()
            #word = word.split()
            for w in word:
                if w not in termsPos:
                   termsPos[w] = 1
                else:
                   termsPos[w] += 1
                if w not in vocab:
                    vocab[w] = 1
                else:
                    vocab[w] += 1

    ## Check for occurences of terms less than 5
    for term in vocab.keys():
        if vocab.get(term) < 5:
            if term in termsPos:
                termsPos.pop(term)
            if term in termsNeg:
                termsNeg.pop(term)


    ## Dump the data into the model
    opFile  = open(model , "w")
    model_data = [termsPos, termsNeg, vocab]
    json.dump(model_data, opFile, indent = 4)
    opFile.close()

    print "Results written in this file ->" , model


if __name__ == '__main__':
    main()
