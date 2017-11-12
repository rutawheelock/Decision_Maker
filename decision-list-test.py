#!/usr/bin/python

"""
CS 5716 PA 4 "Decision Maker"
Program 2: Assigns senses to test data 
Author: Ruta Wheelock
Date: 11/15/2017

Description

"""

import sys

def main()

    # If the user does not provide enought arguments, display message and exit with 1
    if (len(sys.argv) < 2):
        print("Please provide test data as a second command line argument.");
        exit(1);

    test_data = str(sys.argv[1])

    print(test_data);
