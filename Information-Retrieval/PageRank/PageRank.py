__author__ = 'Vikas'

import sys
import math

webgraph = {}                   # webgraph is a dictionary where the key is the Page and the value is the inlinks
Lq = {}                         # Lq is a dictionary where the key is page q and value is the number of out-links
                                # (without duplicates) from page q
S = []                          # S is a list of sink nodes, i.e., pages that have no out links
PR = {}                         # PR is a dictionary where the key is the page and the value is the PageRank value
d = 0.85                        # d is the PageRank damping/teleportation factor
iteration = 4                   # Iteration upto 4 as given in the problem set
Top_Pages = 50                  # Need to find top 50 pages

def main():
    if len(sys.argv) == 2:
        file = str(sys.argv[1])
        Error = True
    else:
        Error = False
        print "Input file required"

    if Error:
        calculatePageRank(file)                              # PAGE RANK Function

def calculatePageRank(file):
    file = open(file, "r")
    i = 0
    j = 0
    for eachNode in file :
        node = eachNode.split()
        P = node[0]
        Mp = node[1:len(node)]
        Mp = list (set(Mp))
        webgraph[P] = Mp

        Lq[P] = 0

    N = float(len(webgraph))
    print "Length of Web Documents ->", N

    for values in webgraph.values():                        # Finding the number of out-links for every page
        for value in values:
            if Lq.has_key(value):
                Lq[value] = Lq[value] + 1
            else:
               Lq[value] = 1
               webgraph[value] = []
               continue


    for page in Lq.keys():                                  # Finding the pages that have no out-links
        if Lq[page] == 0:
            S.append(page)

    for eachPage in webgraph.keys():                        # Initial Page Ranks for each page in the WebGraph
        PR[eachPage] = 1/N

    oldPerplexity = calculatePerplexity(PR)                 # Calculate the initial perplexity
    print 'Perplexity for Iteration 0  : ', oldPerplexity

    while i < iteration:                                    ## PAGE RANK ALGORITHM (4 iterations)
        sinkPR = 0
        newPR = {}
        for eachPage in S:
            sinkPR += PR[eachPage]

        for eachPage in webgraph.keys():
            newPR[eachPage] = (1 - d)/N
            newPR[eachPage] += d * sinkPR/N

            for eachNewPage in webgraph[eachPage]:
                newPR[eachPage] += d * PR[eachNewPage]/Lq[eachNewPage]

        for each in webgraph.keys():
            PR[each] = newPR[each]
        j = j + 1

        newPerplexity = calculatePerplexity(PR)            # Calculate the perplexity after updating the Page Rank values
        print 'Perplexity for Iteration', j ,' : ' ,newPerplexity


        if abs(oldPerplexity - newPerplexity) < 1 :   # Check if the change in the perplexity is less than 1 for 4 iterations
            i += 1
        oldPerplexity = newPerplexity                 # Update the old perplexity

    printResults(PR,webgraph)                         # Print the top 50 Pages


def calculatePerplexity(webgraph):                    # PERPLEXITY CALCULATION
    perplexity = 0
    entropy = 0

    for value in webgraph.values():                   # Finding the Shannon entropy for each inlink
        entropy += - (value * math.log(value, 2))

    perplexity = math.pow(2, entropy)                 # Calulating the perplexity
    return  perplexity


def printResults(PR, webgraph):                       # PRINT RESULTS

    ## Sort the Pages according to their page rank values
    PR_sorted = sorted([(value, key) for key, value in PR.iteritems()],reverse=True)
    ## Sort the Pages according to the number of in-links count
    Inlinks = sorted([(len(value) , key) for key, value in webgraph.iteritems()], reverse = True)
    inlinks_count = 0
    pagerank_count = 0
    initial_pagerank = 1.0/len(PR)
    i=0
    j=0
    print "\nTop 50 pages based on page ranks:"
    for key ,value in PR_sorted:
        i += 1
        print "Page : ", value, " , Rank : ", key
        if(i == Top_Pages):                          ## Top 50 pages based on Page ranks
            break

    print "\nTop 50 pages based on in-links count:"
    for key, value in Inlinks:
        j += 1
        print "Page : ", value, " , In-Link Count : ", key
        if(j == Top_Pages):                         ## Top 50 pages based on in-inlinks count
            break

    for key in webgraph.keys():                     ## Count of Pages that have no in-links
        if(len(webgraph[key]) == 0):
            inlinks_count += 1

    for value in PR.values():                       ## Count of pages whose page rank is less than initial page rank value
        if(value < initial_pagerank):               ## i.e., 1/Total count of Web Pages
            pagerank_count += 1

    ## Proportion of pages with no in-links is Count of Pages with no in-links / Total count of Pages in the web Document
    inlinks_count = float(inlinks_count)/float(len(webgraph.keys()))
    print "\nProportion of pages with no in-links (sources) ->" , inlinks_count

    ## Proportion of pages with no out-links is Count of Pages with no out-links / Total count of Pages in the web Document
    outlinks_count = float(len(S))/float(len(webgraph.keys()))
    print "\nProportion of pages with no out-links (sinks) ->" , outlinks_count

    ## Proportion of pages whose PageRank is less than their initial, uniform values is
    ## Count of Pages whose (Page Rank value < Initial Page Rank) / Total count of Pages in the web Document
    pagerank_count = float(pagerank_count)/float(len(webgraph.keys()))
    print "\nProportion of pages whose PageRank is less than their initial, uniform values -> " , pagerank_count

if __name__ == '__main__':
    main()