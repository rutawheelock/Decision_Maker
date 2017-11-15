#!/usr/bin/python

"""
CS 5761 PA 4 "Decision Maker"
Program 2: Assigns senses to test data 
Author: Ruta Wheelock
Date: 11/15/2017

Description:
This program examins the content of test data and assigns a word sense
to the target word based on decision list.

To run the program, execute:
$ ./decision-list-test.py decision-list.txt test-data.txt
The second command line argument is a name of the decision list file.
Third argument is the training data file.

Program writes answers to standard output.
To write answers in a file, execute:
$ ./decision-list-test.py decision-list.txt test-data.txt > answers.txt

Algorithm:
Adjacent words to the target word are extracted from the test file.
Then each word is looked at the decision list starting from the top.
When one of the words if found in the decision list, approprite sense is 
assigned to the targed word.

Example:
Sample output (first 5 lines) to the following command:
$ ./decision-list-test.py interest-n-decision-list.txt interest-n-test.txt
<answer instance="interest-n.int1585" senseid="interest_5"/>
<answer instance="interest-n.int1724" senseid="interest_5"/>
<answer instance="interest-n.int1555" senseid="interest_5"/>
<answer instance="interest-n.int2260" senseid="interest_5"/>
<answer instance="interest-n.int1847" senseid="interest_5"/>

Output is formatted according to the key file provided for this assignment.

"""

import sys

def main():

    # If the user does not provide enought arguments, display message and exit with 1
    if (len(sys.argv) < 3):
        print "Please provide decision list and test data as a second and third command line arguments."
        exit(1);

    # Read in file names
    decision_list_file = str(sys.argv[1])
    test_file = str(sys.argv[2])

    # Open files
    decision_list = open(decision_list_file, 'r')
    test_data = open(test_file, 'r')

    # Split decision list into lines
    decisions = decision_list.read().splitlines()

    # Declare variables for input processing
    id_code = ''
    previous_line = 'previouslinehere'
    senseid = ''

    # Look through the test data file
    for line in test_data:
        # Retrieve an instance code from <instance> tag
        if line[:9] == '<instance':
            id_code = line.partition('instance id=')[2].rstrip(">\n")

        # Find adjacent words to the target word
        if previous_line[:9] == '<context>':
            left_side = line.partition('<head>')[0].split()
            right_side = line.partition('</head>')[2].split()

            nearby_words = [left_side[-1].strip('.,!"-?'), right_side[0].strip('.,!"-?')]

            found_match = False

            # Loop through the decision list until
            # one of the adjacent words is found
            for decision in decisions:
                # Split the line
                dec_list = decision.split()
                keyword = dec_list[1]
                # Loop through adjacent word list
                for near_word in nearby_words:
                    # If the word is found in decision list,
                    # save the corresponding sense
                    if near_word == keyword:
                        senseid = '"{}"'.format(dec_list[2])
                        found_match = True
                if (found_match):
                    break

            # Print the answer
            print "<answer instance={} senseid={}/>".format(id_code, senseid)
            
        previous_line = line

    # Close files
    decision_list.close()
    test_data.close()

if __name__ == "__main__":
    main()
