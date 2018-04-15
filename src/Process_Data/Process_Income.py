# Import necessary packages here
import sys

# =============================================================================================
# =============================================================================================
# Date:    December 26, 2017
# Purpose: This class processes income data

# Source Code Metadata
__author__ = "Jonathan A. Webb"
__copyright__ = "Copyright 2017, Jon Webb Inc."
__version__ = "1.0"
# =============================================================================================
# =============================================================================================


class ProcessIncome:
    def __init__(self, base_income, filing_state, pay_period):
        self.filing_state = filing_state

        if pay_period.upper() == 'MONTHLY':
            self.base_income = base_income / 12
        elif pay_period.upper() == 'BIMONTHLY':
            self.base_income = base_income / 24
        elif pay_period.upper() == 'TWO_WEEK':
            self.base_income = base_income / 26
        else:
            sys.exit('FATAL ERROR: Pay Period not entered correctly')
        return
# ---------------------------------------------------------------------------------------------
    def net_pay(self, dental, medical, four_o_one_k):
        fed_tax = self.__federal_income_tax()
        state_tax = self.__state_income_tax()
        medicare = self.__medicare()
        social_security = self.__social_security()

        paycheck = self.base_income - fed_tax - state_tax - medicare - social_security - \
                   dental - medical - four_o_one_k
        return paycheck
# ---------------------------------------------------------------------------------------------

    def __federal_income_tax(self):
        percent_tax = 19.534/100.0  # Percent of income
        return self.base_income * percent_tax
# ---------------------------------------------------------------------------------------------

    def __state_income_tax(self):
        percent_tax = 0.0
        if self.filing_state == 'Utah':
            percent_tax = 4.566/100.0  # Percent of income
        return self.base_income * percent_tax
# ---------------------------------------------------------------------------------------------

    def __social_security(self):
        percent_tax = 6.032/100.0  # Percent of income
        return self.base_income * percent_tax
# ---------------------------------------------------------------------------------------------

    def __medicare(self):
        percent_tax = 1.411/100.0  # Percent of income
        return self.base_income * percent_tax
# =============================================================================================
# =============================================================================================
# eof
