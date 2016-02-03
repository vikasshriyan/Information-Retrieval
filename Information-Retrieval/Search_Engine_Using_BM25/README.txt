ASSIGNMENT 3 : SEARCH ENGINE
VIKAS SHRIYAN
001757981
SECTION - 01

=> Use the below two commands to run the program on the terminal. Keep all the files in the same folder.

1. indexer.py

python indexer.py <tccorpus_file_name> <index_file_name>

e.g., python indexer.py tccorpus.txt index.out


=> The index.out file will contain the inverted index for the text document given.
   The program takes about 8 seconds to terminate. 	


2. bm25.py

python bm25.py <index_file_name> <queries_file> <maximum number of document results> <output_file_name>

e.g., python bm25.py index.out queries.txt 100 results.eval

=> The results.eval will contain the top 100 document IDs and their bm25 scores.