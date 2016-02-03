ASSIGNMENT 5 : To evaluate retrieval effectiveness
VIKAS SHRIYAN
001757981
SECTION - 01

COLLABORATED WITH JYOTHI NAMA MAHESH
****************************************************************************************************************

-> Instructions on how to run the program:

python hw5.py <relevance_judgements_file_name> <results_of_bm25_file_name>

e.g., python hw5.py cacm.rel.txt results.eval

=> This program takes in two command line arguments. The first one is the file which contains relevance judgement information
   and second file which contains query results of the IR system of your choice.

****************************************************************************************************************
-> Explanation of the code:

The implementation is straightforward:

=> First I parse two files input by the user.
   Relevance judgement information (cacm.re.txt) : the data in this file is read and stored as Dictionary. Each entry is a key-value pair with queryID as key and list of DocIDs as value.
                                                   The name of the dictionary in the program is relevantDocs.
   Query Result Information (results.eval) : the data in this file is read and stored as an Ordered dictionary(so that order is maintained based on query IDs)
                                             where queryID is key and the value is a dictionary with docID as key and the bm25 score as value.
                                             The name of the dictionary in the program is resultsDict.

=> Then by iterating through the "resultsDict" data structure, I compute the requires precision, recall, and NDCG values.
   Since the values are in the order of insertion (order of rank) the values computed are in the order of rank.

=> Precision is the proportion of relevant documents that are retrieved (relevant found so far / retrieved so far)

=> Recall is the proportion of retrieved documents that are relevant (relevant found so far / total relevant)

=> NDCG = DCG/IDCG; where DCG (at rank r) = relevance of document at rank 1 + SUM[relevance level of doc i/log (base 2) i]{i ranges from 2 -> r}
   ;IDCG is calculated using same formula as DCG, except that the ranking of documents are done such that
    all relevant documents are retrieved first before any irrelevant document.
   ;as the name suggests, this is a cumulative gain measure. Hence the value computed at the previous rank is used to compute
    the current value (as seen in the variables prevDCG , prevIDCG)

=> Finally, p@k for rank 20 is stored in a list and the precision value is added to this list when it is computed at that rank
   for MAP, the AvP for each query is calculated and averaged to obtain the value.

****************************************************************************************************************

Submitted Files:

1.) Source Code -> hw5.py
2.) "Results(2).txt" which contains the 3 tables (1 per query) with computed values for precision, recall and NDCG
3.) "Results(3).txt" which contains the values for p@k and MAP and explaining how I computed the same.
4.) "cacm.re.txt" which contains the relevance judgement information
5.) "results.eval" which contains the results of BM25 assignment. For this assignment only first three queries were
    required and that what is there in this file. Also, to match the queries, the IDs from BM25 ranking is mapped onto its
    corresponding IDs using the "if-else" block in the loadFiles function.
