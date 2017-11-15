#!/usr/bin/python

"""
CS 5761 PA 4 "Decision Maker"
Program 1: Builds decision list from training data
Author: Ruta Wheelock
Date: 11/15/2017

Description:
This program builds decision list using training data for word sense disambiguation.
Program expects training data in a specfic format that was provided for this assignment.

To run the program, execute:
$ ./decision-list-train.py trainig-data.txt
The second command line argument is a name of training data, which is located in the same
directory where this program.

Program writes decision list to the standard output.
To write the decision list in a file, execute:
$ ./decision-list-train.py trainig-data.txt > decision-list.txt

Algorithm:
Decision list is based on adjacent word likelihood to predict a word sense to the target word.
The program collects adjacent words to the target word and calculates
their log-likelihood as decribed in David Yarowsky paper "Decision Lists for Lexical Ambiguity
Resolution". If multiple words have the same log-likelihood, adjacent word count is used for ranking.

Example:
Sample output (first 5 lines) to the following command:
$ ./decision-list-train.py interest-n-train.txt 
2.30258509299 short interest_5 36
2.30258509299 minority interest_5 22
2.30258509299 has interest_5 17
2.30258509299 equity interest_5 13
2.30258509299 open interest_5 8

Each line in decision list has four items:
The first item is a log-likelihood of the adjacent word to determine word sense.
Second item an adjacent word.
Third item is a word sense that the adjacent word predicts.
Fourth item is a number of instances the adjacent word was encountered.

Limitations:
The program is hardcoded to consider only two senses to disambiguate.
If the training data contains more senses, only two will be considered.

"""

from __future__ import division
import sys
from math import fabs, log
from operator import itemgetter

def main():

    # If the user does not provide enought arguments, display message and exit with 1
    if (len(sys.argv) < 2):
        print "Please provide training data as a second command line argument."
        exit(1);

    # Save training data file name
    train_file = str(sys.argv[1])


    #----------------------------
    # Process training data file
    #----------------------------

    # Open the training file
    train_data = open(train_file, 'r')
    
    # Declare variables for line operations
    senses_list = []
    previous_line = 'previouslinehere'
    sense = ''
    collocation_tuples = []

    # Read in every line in training data
    for line in train_data:
        # Look for word sense in <answer> tag and save it
        if line[0:7] == '<answer':
            sense = line.split('senseid=')[1][1:-4]
            senses_list.append(sense)

        # If the previous line was <context>, this line should contain the target word
        if previous_line[:9] == '<context>':
            left_side = line.partition('<head>')[0].split()
            right_side = line.partition('</head>')[2].split()

            # Strip special characters from adjacent words and save words in a list
            nearby_words = [left_side[-1].strip(',.!"-?'), right_side[0].strip(',.!"-?')]

            # If the adjacent word is not an empty string, append it to collocation_tuples
            # with corresponding target word sense
            for word in nearby_words:
                if word != '':
                    collocation_tuples.append((word,sense))
            
        previous_line = line


    # Close training data file
    train_data.close()


    #----------------------------
    # Build decision list
    #----------------------------

    decision_list = []

    # Create a set of adjacent word so that each word can be looked
    # at only once
    set_of_nearby_words = set(x[0] for x in collocation_tuples)
    
    # Create a set of senses and save them in variables
    set_of_senses = set(x[1] for x in collocation_tuples)
    sense_1 = set_of_senses.pop()
    sense_2 = set_of_senses.pop()    

    # Loop through a set of adjacent words
    for word in set_of_nearby_words:
        # Count how many times the word was encountered with one of the senses
        # in training data
        sense_1_count = collocation_tuples.count((word, sense_1))
        sense_2_count = collocation_tuples.count((word, sense_2))
        total_count = sense_1_count + sense_2_count

        # Calculate probability for each sense
        p_sense_1 = sense_1_count/total_count
        p_sense_2 = sense_2_count/total_count

        # Apply smoothing for zero probalilities
        # According to Yarowski, p: 0.1 - 0.25 is appropriate
        if p_sense_1 == 0:
            p_sense_1 = 0.1

        if p_sense_2 == 0:
            p_sense_2 = 0.1

        # Determine which sense was encountered more oftem
        classification = sense_1
        if sense_2_count > sense_1_count:
            classification = sense_2

        # Calculate log-likelihood for this word
        log_likelihood = abs(log(p_sense_1/p_sense_2))

        # Determine whether the word is informative
        # If the log-likelihood is 0, adjacent word is not informative
        # If the word is informative, add it to the decision list
        if log_likelihood != 0.0 and total_count > 1:
            decision_list.append((log_likelihood, word, classification, total_count))
        

    # Sort the decision list based on log-likelihood and the number of times
    # an adjacent word was encountered
    sorted_decision_list = sorted(decision_list, key=itemgetter(0,3), reverse=True)

    # Write the decision list to the standard output
    for decision in sorted_decision_list:
        print decision[0], decision[1], decision[2], decision[3]
            

if __name__ == "__main__":
    main()
