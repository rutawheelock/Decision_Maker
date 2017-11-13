#!/usr/bin/python

"""
CS 5761 PA 4 "Decision Maker"
Program 3: Evaluates test data
Author: Ruta Wheelock
Date: 11/15/2017

Description:


"""

from __future__ import division
import sys


def main():

    # Check if enought command line argumenrs are provided
    if (len(sys.argv) < 3):
        print "Please provide key data and answers as a second and third command line arguments."
        exit(1);

    key_file = str(sys.argv[1])
    answer_file = str(sys.argv[2])

    key_data = open(key_file, 'r')
    answer_data = open(answer_file, 'r')

    keys = key_data.read().splitlines()
    answers = answer_data.read().splitlines()

    set_of_senses = set()
    for key in keys:
        set_of_senses.add(key.split()[2])
        
    sense_1_raw = set_of_senses.pop()
    sense_2_raw = set_of_senses.pop()
    
    sense_1 = sense_1_raw.rstrip('"/>\n').partition('senseid="')[2]
    sense_2 = sense_2_raw.rstrip('"/>\n').partition('senseid="')[2]

    total = 0
    correct = 0
    sense_1_wrong = 0
    sense_2_wrong = 0
    for i in range(len(keys)):
        if keys[i] == answers[i]:
            correct += 1
        elif keys[i].split()[2] == sense_1_raw:
            sense_1_wrong += 1
        else:
            sense_2_wrong += 1

        total += 1


    correct_perc = round(correct/total*100, 2)
        
    print "Total count: {}".format(total)
    print "Correct count: {}".format(correct,)
    print "Accuracy: {}% \n".format(correct_perc)
    print "Confusion Matrix: (raw counts)"
    longest_w = max(len(sense_1), len(sense_2))
    dist_1 = 2*longest_w
    print "-"*longest_w + '| {} | {}'.format(sense_1, sense_2)
    print "{}".format(sense_1) + " "*dist_1 + "{} ".format(sense_1_wrong)
    print "{}     {}".format(sense_2, sense_2_wrong)


    # Close files
    key_data.close()
    answer_data.close()

                                      
if __name__ == "__main__":
    main()








    
