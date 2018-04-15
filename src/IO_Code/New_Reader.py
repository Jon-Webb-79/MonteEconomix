# Import necessary packages here
from IO_Code.Reader import read_text_file_by_keywords, verify_file_existance
from datetime import date

import sys
import pandas as pd
# =============================================================================================
# =============================================================================================
# Date:    December26, 2017
# Purpose: This code contains functions necessary to read in .txt and .csv files

# Source Code Metadata
__author__ = "Jonathan A. Webb"
__copyright__ = "Copyright 2017, Jon Webb Inc."
__version__ = "1.0"
# =============================================================================================
# =============================================================================================


class ReadPayInformation:
    def read_pay_data(self, input_file, inputfile):
        """

        :param input_file: char str
                           The file containing the input data to include the \
                           absolute or relative path length
        :param inputfile: char str
                          The input container
        :return NA:

        This function reads in all variable input data
        """
        inputfile.sample_size = read_text_file_by_keywords(input_file, 'Sample Size:', 'INTEGER')
        inputfile.start_date = read_text_file_by_keywords(input_file, 'Start Date:', 'STRING')
        inputfile.end_date = read_text_file_by_keywords(input_file, 'End Date:', 'STRING')
        inputfile.checking_start = read_text_file_by_keywords(input_file,
                                                              'Checking Start Value:',
                                                              'FLOAT')
        inputfile.savings_start = read_text_file_by_keywords(input_file,
                                                             'Savings Start Value:',
                                                             'FLOAT')
        inputfile.base_salary = read_text_file_by_keywords(input_file,
                                                           'Annual Base Salary:',
                                                           'FLOAT')
        inputfile.pay_period = read_text_file_by_keywords(input_file,
                                                          'Pay Period:',
                                                          'STRING')
        inputfile.dental_deduction = read_text_file_by_keywords(input_file,
                                                                'Dental Deduction:',
                                                                'FLOAT')
        inputfile.medical_deduction = read_text_file_by_keywords(input_file,
                                                                 'Medical Deduction:',
                                                                 'FLOAT')
        inputfile.fok_deduction = read_text_file_by_keywords(input_file,
                                                             '401k Deduction:',
                                                             'FLOAT')
        inputfile.hist_start_date = read_text_file_by_keywords(input_file,
                                                               'Hist Start Date:',
                                                               'STRING')
        inputfile.hist_end_date = read_text_file_by_keywords(input_file,
                                                             'Hist End Date:',
                                                             'STRING')
        inputfile.filing_state = read_text_file_by_keywords(input_file,
                                                            'Filing State:',
                                                            'STRING')
        inputfile.histogram_bins = read_text_file_by_keywords(input_file,
                                                              'Histogram Bins:',
                                                              'INTEGER')
        inputfile.first_check = read_text_file_by_keywords(input_file,
                                                           'First Check:',
                                                           'STRING')

        if inputfile.filing_state == 'NA':
            sys.exit('FATAL ERROR: Filing State not properly entered')
        inputfile.first_check = self.__create_datetime(inputfile.first_check)

        inputfile.start_date = self.__create_datetime(inputfile.start_date)
        inputfile.end_date = self.__create_datetime(inputfile.end_date)
        delta = (inputfile.end_date - inputfile.start_date).days
        if delta < 0:
            sys.exit("FATAL ERROR: Start Date is before End Date!")

        inputfile.hist_start_date = self.__create_datetime(inputfile.hist_start_date)
        inputfile.hist_end_date = self.__create_datetime(inputfile.hist_end_date)
        delta = (inputfile.hist_end_date - inputfile.hist_start_date).days
        if delta < 0:
            sys.exit("FATAL ERROR: Start Date is before End Date!")
        return
# ---------------------------------------------------------------------------------------------
    # Read bills

    def read_bills(self, file):
        """

        :param file: char str
                     The bills file name to include the full absolute \
                     or relative path length
        :return data: object
                      The pandas dataframe containing the bills data

        This function reads in all bills related data
        """
        verify_file_existance(file)
        data = pd.read_csv(file, dtype={'Amount': float, 'Day': int,
                                        'Description': str})
        data = data.set_index("Day")
        return data
# ---------------------------------------------------------------------------------------------
    # Read bills

    def read_planned_expenses(self, file):
        """

        :param file: char str
                     The expense file name to include the full absolute \
                     or relative path length
        :return data: object
                      The pandas dataframe containing the planned expense \
                      data

        This function reads in all planned expense related data
        """
        verify_file_existance(file)
        data = pd.read_csv(file, parse_dates=[0], dtype={'Date': str, 'Debit': float,
                                                         'Addition': float,
                                                         'Description': str})
        data = data.set_index("Date")
        return data
# ---------------------------------------------------------------------------------------------
    # Read histogram data

    def read_histograms(self, file):
        """

        :param file: char str
                     The histogram file name to include the full absolute \
                     or relative path length
        :return data: object
                      The pandas dataframe containing the histogram data \

        This function reads in all planned expense related data
        """
        verify_file_existance(file)
        data = pd.read_csv(file, parse_dates=[0], dtype={'Date': str, 'Bar': float,
                                                         'Gas': float,
                                                         'Groceries': float,
                                                         'Misc': float,
                                                         'Restaurant': float})
        data = data.set_index("Date")
        return data
# ---------------------------------------------------------------------------------------------
    # Transforms date from a string to a datetime object

    def __create_datetime(self, start_date):
        """

        :param start_date: char str
                           The start date (Year, Month, Day)
        :return new_date: The start date as a datetime.date object
        """
        months = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5,
                  'June': 6, 'July': 7, 'August': 8, 'September': 9, 'October': 10,
                  'November': 11, 'December': 12}
        if start_date.upper() == 'TODAY':
            new_date = date.today()
        else:
            calendar = start_date.split()
            day = int(calendar[0])
            month = months[calendar[1]]
            year = int(calendar[2])
            new_date = date(year, month, day)
        return new_date
# ---------------------------------------------------------------------------------------------
# eof
