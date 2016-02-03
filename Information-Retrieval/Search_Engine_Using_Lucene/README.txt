ASSIGNMENT 4 : Introduction to Lucene: Setup, indexing, search
	       Zipf’s law
VIKAS SHRIYAN
001757981
SECTION - 01

COLLABORATED WITH JYOTHI PRASAD NAMA MAHESH

**********************************************************************
Instructions to run the code:

-> The program requires three external libraries (lucene-core-4.7.2.jar,lucene-queryparser-4.7.2.jar,lucene-analyzers-common-4.7.2.jar), 
   which is provided with my code. Remember to keep all the three files and the HW.java file in the same folder.

1.) Compile the code using the following command:

    javac -cp lucene-core-4.7.2.jar:lucene-queryparser-4.7.2.jar:lucene-analyzers-common-4.7.2.jar:jsoup-1.8.3.jar HW4.java


2.) Execute the code using the following command:

    java -cp .:lucene-core-4.7.2.jar:lucene-queryparser-4.7.2.jar:lucene-analyzers-common-4.7.2.jar:jsoup-1.8.3.jar HW4


No command line arguments required for this program but it asks inputs when running.
The printed statement will explain what inputs it expects.

***********************************************************************
Explanation about the code added:

-> For this implementation, we make use of Lucene’s “SimpleAnalyzer” that ignores non-letters or digits and special characters while indexing the corpus. There are analyzers like the standard analyzer but for this assignment purpose we make use of simple analyzer.

-> The program creates and index from the set of these files “.html,.htm,.xml,.txt” that is provided as an input when prompted for (In this case we provide CACM corpus which is also included in the submission). Before indexing, we remove “html” and “pre” tags using Jsoup so that these don’t form the part of the text corpus and rewrite  the input file.
**Note : Do not create the index multiple times. This results in duplication of information. 

-> From the generated index, we create a HashMap of the terms and their term frequencies in descending order of their term frequencies.

-> Next, we take the query input one at a time, to generate the top 100 ranked documents. But before doing this the query string is checked for special characters and numbers that are removed and all the characters are converted to lower case. The ranked documents are displayed with the file name and the score. 

***********************************************************************
Submitted output Files:

1.) README.txt

2.) Source code is the “HW4.java” with 4 dependency libraries as mentioned above.

3.) The sorted (by frequency) list of (term, term_freq pairs) are provided in the “Lucene_Term_TermFrequencies.txt” file.

4.) Plot of the resulting Zipfian curve (Plotted on log-log graph where x-axis is the rank of word and y-axis is the total number of occurrences of the word) is provided in the “Zipfian_Curve.pdf” file.

5.) List of Top 100 docIDs ranked by score for the given queries is present in the “Queries_Result.txt” file.

6.) Table comparing the total number of documents retrieved per query using Lucene’s scoring function vs. BM25 search engine is present in the “Comparison_BM25_Lucene.pdf” file.


