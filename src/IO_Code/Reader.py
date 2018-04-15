# Import necessary packages here
import os
import sys
import csv
import numpy as np
# =============================================================================================
# =============================================================================================
# Date:    November 10, 2017
# Purpose: This code contains functions necessary to read in .txt and .csv files

# Source Code Metadata
__author__ = "Jonathan A. Webb"
__copyright__ = "Copyright 2017, Jon Webb Inc."
__version__ = "1.0"
# =============================================================================================
# =============================================================================================


def verify_file_existance(file_name):
    """
    :param file_name : char string
                       the pathlink to a file
    :return:

    This function tests a file-directory-path to ensure that
    the file actually exists
    """
    if os.path.isfile(file_name):
        return
    sys.exit('{}{}{}'.format('FATAL ERROR: ', file_name, ' does not exist'))
# ---------------------------------------------------------------------------------------------


def read_csv_by_header(file_name, header, data_type):
    """
    :param file_name : char string
                       The name of the .csv file to be opened (must include .csv in the name)
    :param header : char
                    The header which identifies the column to be read
    :param data_type : char
                       The data type, which the column is to be converted to.
                       Can be FLOAT, DOUBLE, INTEGER, or STRING
    :return: column : user defined
                      The array of data read in by the function.

    This function opens a .csv file and reads in the column identified by a user
    defined header
    """
    # Check for errors
    verify_file_existance(file_name)
    column = []
    with open(file_name) as Input_File:
        reader = csv.DictReader(Input_File)
        for row in reader:
            column.append(row[header])
    if data_type.upper() == 'FLOAT':
        column = np.array(column, np.dtype(np.float32))
    elif data_type.upper() == 'DOUBLE':
        column = np.array(column, np.dtype(np.float64))
    elif data_type.upper() == 'INTEGER':
        column = np.array(column, np.dtype(np.int))
    elif data_type.upper() == 'STRING':
        column = np.array(column)
    else:
        sys.exit("Data type not properly entered into 'read_csv_by_header()' function")
    return column
# ---------------------------------------------------------------------------------------------

def read_text_file_by_keywords(file_name, key_words, data_type):
    verify_file_existance(file_name)
    input_words = key_words.split()

    with open(file_name) as Input_File:
        lines = Input_File.readlines()
        for line in lines:
            variable = line.split()
            #print(variable)
            counter = 0
            for i in range(len(input_words)):
                if input_words[i] != variable[i]:
                    break
                else:
                    counter = counter + 1
            if counter == len(input_words) and data_type.upper() == 'INTEGER':
                return np.int(variable[len(input_words)])
            elif counter == len(input_words) and data_type.upper() == 'FLOAT':
                return np.float32(variable[len(input_words)])
            elif counter == len(input_words) and data_type.upper() == 'DOUBLE':
                return np.float64(variable[len(input_words)])
            elif counter == len(input_words) and data_type.upper() == 'STRING':
                start = len(input_words)
                end = len(variable)
                word = ''
                for i in range(start, end):
                    word = word + ' ' + variable[i]
                return(word.lstrip())
    sys.exit('{}{}{}'.format(key_words, " Keywords not found in ", file_name))
# =============================================================================================
# =============================================================================================
# eof
