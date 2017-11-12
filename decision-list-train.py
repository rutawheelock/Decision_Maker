#!/usr/bin/python

"""
CS 5716 PA 4 "Decision Maker"
Program 1: Builds decision list from training data
Author: Ruta Wheelock
Date: 11/15/2017

Description:

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
    # Get the word for sense disambiguation
    main_word = train_file.split('-')[0]

    # Open the training file
    train_data = open(train_file, 'r')

    # Declare scope variables for line operations
    senses_list = []
    previous_line = 'somethinghere'
    test_count = 0
    sense = ''
    collocation_tuples = []
    
    for line in train_data:
        if line[0:7] == '<answer':
            sense = line.split('senseid=')[1][1:-4]
            senses_list.append(sense)

        if previous_line[:9] == '<context>':
            left_side = line.partition('<head>')[0].split()
            right_side = line.partition('</head>')[2].split()

            nearby_words = [left_side[-1].strip(',.!"-?'), right_side[0].strip(',.!"-?')]

            for word in nearby_words:
                if word != '':
                    collocation_tuples.append((word,sense))
                    #print collocation_tuples[-1]
            
        previous_line = line


    #----------------------------
    # Build decision list
    #----------------------------
    # !!!! Note - Hard coded for only 2 senses!!!

    decision_list = []

    set_of_nearby_words = set(x[0] for x in collocation_tuples)
    set_of_senses = set(x[1] for x in collocation_tuples)
    sense_1 = set_of_senses.pop()
    sense_2 = set_of_senses.pop()    
        
    for word in set_of_nearby_words:
        sense_1_count = collocation_tuples.count((word, sense_1))
        sense_2_count = collocation_tuples.count((word, sense_2))
        total_count = sense_1_count + sense_2_count

        p_sense_1 = sense_1_count/total_count
        p_sense_2 = sense_2_count/total_count
#        print "P1: {}, P2: {}".format(p_sense_1, p_sense_2)

        # smoothing
        if p_sense_1 == 0:
            p_sense_1 = 0.0001

        if p_sense_2 == 0:
            p_sense_2 = 0.0001

        classification = sense_1
        if sense_2_count > sense_1_count:
            classification = sense_2
            
        log_likelihood = abs(log(p_sense_1/p_sense_2))

        if log_likelihood != 0.0 and total_count > 1:
            decision_list.append((log_likelihood, word, classification, total_count))
        
 #       print "Word: {}, Sense_1: {}, Sense_2: {}, Total: {}".format(word, sense_1_count, sense_2_count, total_count)
 #       print "P1: {}, P2: {}, log_lkh: {}, class: {}".format(p_sense_1, p_sense_2, log_likelihood, classification)


        
    # Find how many senses were found
#    senses_set = set(senses_list)
#    print "Number of instances: {}".format(len(senses_list))
#    for sense in senses_set:
#        print "Number of {meaning} senses: {count}".format(meaning=sense,
#                                                           count=senses_list.count(sense))

    sorted_decision_list = sorted(decision_list, key=itemgetter(0,3), reverse=True)
    
    for decision in sorted_decision_list:
        print decision[0], decision[1], decision[2], decision[3]
        

    # for testing
    #for entry in collocation_tuples:
    #    word = entry[0]
    #    if word == 'a':
    #        print entry

    
    # Close training data file
    train_data.close()
    

if __name__ == "__main__":
    main()
