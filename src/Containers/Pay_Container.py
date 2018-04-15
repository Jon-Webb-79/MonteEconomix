# Import necessary packages here

# =============================================================================================
# =============================================================================================
# Date:    December 26, 2017
# Purpose: This class contains variables relevant to paycheck information

# Source Code Metadata
__author__ = "Jonathan A. Webb"
__copyright__ = "Copyright 2017, Jon Webb Inc."
__version__ = "1.0"
# =============================================================================================
# =============================================================================================


class PayContainer:
    def __init__(self):
        self.sample_size = 0
        self.start_date = '01 January 2000'
        self.end_date = '01 January 2000'
        self.checking_start = 0
        self.savings_start = 0
        self.base_salary = 0
        self.pay_period = 'Bimonthly'
        self.dental_deduction = 0
        self.medical_deduction = 0
        self.fok_deduction = 0
        self.hist_start_date = '01 January 2000'
        self.hist_end_date = '01 January 2000'
        self.filing_state = 'NA'
        self.histogram_bins = 60
        self.fist_check = 'NA'
        return
# =============================================================================================
# =============================================================================================
# eof
