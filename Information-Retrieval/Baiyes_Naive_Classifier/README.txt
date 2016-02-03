ASSIGNMENT 6 : Text Classification
VIKAS SHRIYAN (001757981) & ABHISHEK KUMAR (001735698)

SECTION - 01

COLLABORATED WITH ABHISHEK KUMAR
****************************************************************************************************************

-> Instructions on how to run the program:

Program 1:
----------

    python nbtrain.py <training-directory> <model-file>

    e.g., python nbtrain.py textcat_train model_file_test

    => This program takes in two command line arguments. The first one is the directory which contains the training negative
    and positive review files and the second parameter is the output file in which model data is stored. The model data contains
    the negative review hashmap, positive review hashmap and the vocabulary hashmap.


Program 2:
----------

    python nbtest.py <model-file> <test-directory> <predictions-file>

    Example 1: python nbtest.py model_file_test test Predictions_File_Test

    => This program takes in three command line arguments. The first one is the file which contains the model data.
    The second argument is the test directory in this example. The third parameter is the output file name in which the
    output is written. The output here is the list of text files and the positive and negative review probability values.
    And the output will also be printed on the console which is the top 20 terms, the negative review accuracy and positive
    review accuracy.

    Example 2: python nbtest.py model_file_test dev/pos Predictions_File_Dev_Pos

    => This program takes in three command line arguments. The first one is the file which contains the model data.
    The second argument is the dev positive directory in this example. The third parameter is the output file name in which the
    output is written. The output here is again the list of text files and the positive and negative review probability values
    for the positive reviews. And the output will also be printed on the console which is the top 20 terms, the negative review accuracy and positive
    review accuracy.

    Example 3: python nbtest.py model_file_test dev/neg Predictions_File_Dev_Neg

    => This program takes in three command line arguments. The first one is the file which contains the model data.
    The second argument is the dev negative directory in this example. The third parameter is the output file name in which the
    output is written. The output here is again the list of text files and the positive and negative review probability values
    for the negative reviews. And the output will also be printed on the console which is the top 20 terms, the negative review accuracy and positive
    review accuracy.

****************************************************************************************************************

Output Explanation:

When you run the above steps on the development directory, the program outputs are as below:

Positive Review Output (when run the Example 2):

    Negative Review Accuracy -> 26 % Positive Review Accuracy -> 75 %

Negative Review Output (when run the Example 3):

    Negative Review Accuracy -> 75 % Positive Review Accuracy -> 26 %

****************************************************************************************************************

Submitted Files:

1.) Source Code -> nbtrain.py and nbtest.py
2.) "Predictions_File_Test.txt" which contains the list of files and the positive and negative probability values for test data.
3.) "Predictions_File_Dev_Neg.txt: which contains the list of files and the positive and negative probability values for negative development data.
4.) "Predictions_File_Dev_Pos.txt: which contains the list of files and the positive and negative probability values for positive development data.
5.) "PositiveToNegative.txt: which contains a list of the 20 terms with the highest (log) ratio of positive to negative weight.
6.) "NegativeToPositive.txt: which contains a list of the 20 terms with the highest (log) ratio of negative to positive  weight.
7.) "model_file_test.txt" which contains the model data used in the nbtest program.
