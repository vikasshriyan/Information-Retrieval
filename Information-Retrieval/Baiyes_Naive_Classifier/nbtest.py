__author__ = 'Vikas'

import sys
import json
import glob
import math


test_Positive_Prob = {}         ## Dictionary to store the Probabilities for the Positive reviews
                                ## Key -> Term, Value -> Probability value

test_Negative_Prob = {}         ## Dictionary to store the Probabilities for the Negative reviews
                                ## Key -> Term, Value -> Probability value

test_Review_Files = {}          ## Dictionary to store the positive and negative review
                                ## Key -> File Name, Value -> 1 if Positive, 0 if Negative

pos_To_Neg = {}
neg_To_Pos = {}

def main():

    if len(sys.argv) == 4:
        textcat = sys.argv[2]
        model_file = sys.argv[1]
        output_file = sys.argv[3]
        Error = True
    else:
        Error = False
        print "Three arguments expected"

    if Error:
        loadFiles(textcat,model_file, output_file)

def loadFiles(textcat,model_file,output_file):

    total_Positive_Terms = 0.0
    total_Negative_Terms = 0.0
    total_Terms = 0.0

    ## Load the model File
    modelFile = open(model_file, "r")

    ## Load the two dictionaries from the file.
    ds = json.load(modelFile)
    termsPos = ds[0]
    termsNeg = ds[1]
    vocab = ds[2]


    modelFile.close()

    ## Calculating total number of positive and negative terms
    for value in termsPos.values():
        total_Positive_Terms += value

    for value in termsNeg.values():
        total_Negative_Terms += value

    for value in vocab.values():
        total_Terms += value

    ## Calculate the log ratio of top 20 terms
    for term in vocab:
        if term in termsPos:
            term_Freq_pos = termsPos.get(term)
        else:
            term_Freq_pos = 1.0
        if term in termsNeg:
            term_Freq_neg = termsNeg.get(term)
        else:
            term_Freq_neg = 1.0

        posToNeg = math.log((term_Freq_pos/total_Positive_Terms)/(term_Freq_neg/total_Negative_Terms))
        negToPos = math.log((term_Freq_neg/total_Negative_Terms)/(term_Freq_pos/total_Positive_Terms))
        pos_To_Neg[term] = posToNeg
        neg_To_Pos[term] = negToPos

    sortedpos_To_Neg = sorted([(v , k) for k, v in pos_To_Neg.iteritems()], reverse=True)
    sortedneg_To_Pos = sorted([(v , k) for k, v in neg_To_Pos.iteritems()], reverse=True)
    i = 0
    print "20 terms with the highest (log) ratio of positive to negative weight :"
    for term,value in sortedpos_To_Neg:
        i+=1
        print "term -> " ,  value  ,  " Score -> "  , term
        if i == 20:
            break
    j = 0
    print "20 terms with the highest (log) ratio of negative to positive weight"
    for term, value in sortedneg_To_Pos:
        j += 1
        print "term -> " ,  value  ,  " Score -> "  , term
        if j == 20:
            break

    ## Calculating the total Prior Positive , Negative Prob
    prior_Positive = math.log(float(total_Positive_Terms)/float(total_Terms))
    prior_Negative = math.log(float(total_Negative_Terms)/float(total_Terms))

    ##Load the test directory
    test_path = textcat+'/*.txt'
    test_files = glob.glob(test_path)
    for file in test_files:
        file = open(file, "r")
        posValue = 0.0
        term_Freq_Pos = 1.0
        term_Freq_Neg = 1.0
        negValue = 0.0
        for line in file:
            word = line.split()
            for w in word:
                if w in termsPos:                       ## Check the term for Positive Review
                    term_Freq_Pos = termsPos.get(w)
                    if term_Freq_Pos == 0.0:
                        term_Freq_Pos = 1.0             ## Add Laplace Smoothing
                if w in termsNeg:                       ## Check the term for Negative Review
                    term_Freq_Neg = termsNeg.get(w)
                    if term_Freq_Neg == 0.0:
                        term_Freq_Neg = 1.0             ## Add Laplace Smoothing
                negValue += math.log(float(term_Freq_Neg)/float(total_Negative_Terms))
                posValue += math.log(float(term_Freq_Pos)/float(total_Positive_Terms))
        posValue = posValue + prior_Positive
        negValue = negValue + prior_Negative
        file.close()
        if textcat == "dev/neg" or textcat == "dev/pos":
            test_Positive_Prob[str(file).split("/")[2].split("'")[0]] = posValue
            test_Negative_Prob[str(file).split("/")[2].split("'")[0]] = negValue
        test_Positive_Prob[str(file).split("/")[1].split("'")[0]] = posValue
        test_Negative_Prob[str(file).split("/")[1].split("'")[0]] = negValue

    output_file = open(output_file, 'w')
    displayOutput(test_Positive_Prob, test_Negative_Prob, output_file)
    output_file.close()

    print "Results written in ->" , output_file
    ## Classify the test directory based on Probabilities
    for file in test_Positive_Prob:
        posReview = test_Positive_Prob.get(file)
        negReview = test_Negative_Prob.get(file)
        if posReview > negReview:
            test_Review_Files[file] = 1              ## if positive review
        else:
            test_Review_Files[file] = 0              ## if negative review

   # print test_Review_Files
    negcount = 0
    poscount = 0
    for value in test_Review_Files.values():
        if value == 0:
           negcount += 1
        else:
            poscount += 1
    print "Negative Review Accuracy ->" ,negcount,"%", "Positive Review Accuracy ->", poscount,"%"

def displayOutput(test_Positive_Prob, test_Negative_Prob, output_file):
    headings = "Text ".center(10) +\
                "Positive".rjust(15) +\
                "Negative".rjust(20)
    output_file.write(headings + "\n")

    for file in test_Positive_Prob:

        line =  str(file).center(10) +\
                str(test_Positive_Prob.get(file)).center(15) +\
                str(test_Negative_Prob.get(file)).rjust(20)

        output_file.write(line + "\n")

if __name__ == '__main__':
    main()