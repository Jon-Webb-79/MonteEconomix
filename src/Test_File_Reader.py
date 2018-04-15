# Import modules here
from IO_Code.New_Reader import ReadPayInformation
from Containers.Pay_Container import PayContainer
from datetime import date
import numpy as np
import unittest
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


class TestInputFile(unittest.TestCase):
    def setUp(self):
        self.container = PayContainer()
        self.PI = ReadPayInformation()
        self.input_file = '../Input_Files/Paycheck.txt'
        return
# ---------------------------------------------------------------------------------------------
    # Test input file to see if it reads information correctly

    def test_read_pay_data(self):
        self.PI.read_pay_data('../Data/VandV/Read_Files/Paycheck.txt', self.container)
        self.assertEqual(self.container.sample_size, 10000)
        self.assertEqual(self.container.start_date, date(2017, 3, 1))
        self.assertEqual(self.container.end_date, date(2018, 2, 28))
        self.assertEqual(self.container.checking_start, np.float32(19736.01))
        self.assertEqual(self.container.savings_start, np.float32(2341.95))
        self.assertEqual(self.container.base_salary, np.float32(120000.0))
        self.assertEqual(self.container.pay_period, 'Two_Week')
        self.assertEqual(self.container.dental_deduction, np.float32(8.19))
        self.assertEqual(self.container.medical_deduction, np.float32(165.04))
        self.assertEqual(self.container.fok_deduction, np.float32(291.92))
        self.assertEqual(self.container.hist_start_date, date(2017, 3, 1))
        self.assertEqual(self.container.hist_end_date, date(2017, 12, 26))
        self.assertEqual(self.container.filing_state, 'Utah')
        return
# ---------------------------------------------------------------------------------------------
    # Test for end date before start date

    def test_mixed_dates(self):
        try:
            self.PI.read_pay_data('../Data/VandV/Read_Files/MixedDates.txt', self.container)
            self.assertEqual(1, 0)
        except SystemExit:
            self.assertEqual(1, 1)
        return
# ---------------------------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
