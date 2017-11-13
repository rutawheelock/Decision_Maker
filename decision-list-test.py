#!/usr/bin/python

"""
CS 5761 PA 4 "Decision Maker"
Program 2: Assigns senses to test data 
Author: Ruta Wheelock
Date: 11/15/2017

Description

"""

import sys

def main():

    # If the user does not provide enought arguments, display message and exit with 1
    if (len(sys.argv) < 3):
        print "Please provide decision list and test data as a second and third command line arguments."
        exit(1);

    decision_list_file = str(sys.argv[1])
    test_file = str(sys.argv[2])

    decision_list = open(decision_list_file, 'r')
    decisions = decision_list.read().splitlines()
    test_data = open(test_file, 'r')

    # Declare variables for input processing
    id_code = ''
    previous_line = 'previouslinehere'
    senseid = ''

    for line in test_data:
        if line[:9] == '<instance':
            id_code = line.partition('instance id=')[2].rstrip(">\n")

        if previous_line[:9] == '<context>':
            left_side = line.partition('<head>')[0].split()
            right_side = line.partition('</head>')[2].split()

            nearby_words = [left_side[-1].strip('.,!"-?'), right_side[0].strip('.,!"-?')]

            found_match = False

            for decision in decisions:
                dec_list = decision.split()
                keyword = dec_list[1]
                for near_word in nearby_words:
                    if near_word == keyword:
                        senseid = '"{}"'.format(dec_list[2])
                        found_match = True
                if (found_match):
                    break

            print "<answer instance={} senseid={}/>".format(id_code, senseid)
            
        previous_line = line

    # Close files
    decision_list.close()
    test_data.close()

if __name__ == "__main__":
    main()
