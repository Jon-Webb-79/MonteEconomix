# Import necessary packages here
from Containers.Pay_Container import PayContainer
from IO_Code.New_Reader import ReadPayInformation
from Process_Data.Process_Income import ProcessIncome
import numpy as np
import pandas as pd
import random
import calendar
import scipy.interpolate
# =============================================================================================
# =============================================================================================
# Date:    December 26, 2017
# Purpose: This code integrates all functionality for the MonteEconomix program

# Source Code Metadata
__author__ = "Jonathan A. Webb"
__copyright__ = "Copyright 2017, Jon Webb Inc."
__version__ = "1.0"
# =============================================================================================
# =============================================================================================


def create_cdf(data_array, nbins):
    hist, edges = np.histogram(data_array, bins=nbins, normed=True)
    cdf = np.cumsum(hist * np.diff(edges))
    center = (edges[:-1] + edges[1:]) / 2.0
    cdf = np.concatenate((np.array([0.0]), np.array(cdf)), axis=0)
    center = np.concatenate((np.array([0.0]), np.array(center)), axis=0)
    return cdf, center
# =============================================================================================
# =============================================================================================
# =============================================================================================
# =============================================================================================
# =========================                                       =============================
# =========================     INSTANTIATE NECESSARY CLASSES     =============================
# =========================                                       =============================
# =============================================================================================
# =============================================================================================


pay_container = PayContainer()
PI = ReadPayInformation()
# =============================================================================================
# =============================================================================================
# =========================                                       =============================
# =========================           READ INPUT FILES            =============================
# =========================                                       =============================
# =============================================================================================
# =============================================================================================
PI.read_pay_data('../Input_Files/Paycheck.txt', pay_container)
income = ProcessIncome(pay_container.base_salary,
                       pay_container.filing_state,
                       pay_container.pay_period)
# ---------------------------------------------------------------------------------------------
# Read in normal Bills
bills = PI.read_bills('../Input_Files/Bills.csv')
# ---------------------------------------------------------------------------------------------
# Read in planned expenses
planned = PI.read_planned_expenses('../Input_Files/Planned_Expenses.csv')
# ---------------------------------------------------------------------------------------------
# Read in histogram data
histogram = PI.read_histograms('../../Finances2.0/Input_Files/Histograms/HistFile.csv')
# ---------------------------------------------------------------------------------------------
# Create CDFs for later sampling
misc_cdf, misc_center = create_cdf(histogram['Misc'][pay_container.hist_end_date:pay_container.hist_start_date],
                                   pay_container.histogram_bins)
groc_cdf, groc_center = create_cdf(histogram['Groceries'][pay_container.hist_end_date:pay_container.hist_start_date],
                                   pay_container.histogram_bins)
rest_cdf, rest_center = create_cdf(histogram['Restaurant'][pay_container.hist_end_date:pay_container.hist_start_date],
                                   pay_container.histogram_bins)
gas_cdf, gas_center = create_cdf(histogram['Gas'][pay_container.hist_end_date:pay_container.hist_start_date],
                                 pay_container.histogram_bins)
bar_cdf, bar_center = create_cdf(histogram['Bar'][pay_container.hist_end_date:pay_container.hist_start_date],
                                 pay_container.histogram_bins)
# Create interpolae samples arrays
misc_interp = scipy.interpolate.interp1d(misc_cdf, misc_center)
groc_interp = scipy.interpolate.interp1d(groc_cdf, groc_center)
rest_interp = scipy.interpolate.interp1d(rest_cdf, rest_center)
gas_interp = scipy.interpolate.interp1d(gas_cdf, gas_center)
bar_interp = scipy.interpolate.interp1d(bar_cdf, bar_center)
# =============================================================================================
# =============================================================================================
# =========================                                       =============================
# =========================         INITIALIZE VARIABLES          =============================
# =========================                                       =============================
# =============================================================================================
# =============================================================================================
# Determine the net pay dispersement after deductions
net_pay = income.net_pay(pay_container.dental_deduction,
                         pay_container.medical_deduction,
                         pay_container.fok_deduction)
date_index = pd.date_range(pay_container.start_date, pay_container.end_date)
random.seed(123456)
# =============================================================================================
# =============================================================================================
# =========================                                       =============================
# =========================         MONTE CARLO PROGRAM           =============================
# =========================                                       =============================
# =============================================================================================
# =============================================================================================
checking_account = []
maximum = []
minimum = []
checking_value = pay_container.checking_start
count = False
counter = 0
for x in date_index:

    # Kicks off counter if two week pay period is selected
    if pay_container.pay_period == 'Two_Week' and x.date() == pay_container.first_check:
        count = True
        counter = 14
    if count == True and counter < 14:
        counter += 1

    # Determines if pay should be allocated
    days_in_month = calendar.monthrange(x.year, x.month)[1]
    if pay_container.pay_period == 'Monthly' and days_in_month == x.day:
        checking_value += net_pay
    elif pay_container.pay_period == 'Bimonthly' and x.day == 15 and \
         x.day == days_in_month:
        checking_value += net_pay
    elif pay_container.pay_period == 'Two_Week' and counter == 14:
        checking_value += net_pay
        counter = 0

    # Subtract pay for standard bills
    if x.day in bills.index:
        checking_value -= bills['Amount'][x.day].sum()

    # Subtract for planned expenses
    if x.date() in planned.index:
        checking_value = checking_value + planned['Addition'][x.date()].sum() - \
                         planned['Debit'][x.date()].sum()

    # Subtract random spending with statistics
    misc_expense = misc_interp(np.random.rand(pay_container.sample_size))
    groc_expense = groc_interp(np.random.rand(pay_container.sample_size))
    rest_expense = rest_interp(np.random.rand(pay_container.sample_size))
    bar_expense = bar_interp(np.random.rand(pay_container.sample_size))
    gas_expense = gas_interp(np.random.rand(pay_container.sample_size))

    total = misc_expense + groc_expense + rest_expense + bar_expense + gas_expense
    sigma = np.std(total)

    checking_value = checking_value - np.mean(total)

    checking_account.append(round(float(checking_value), 2))
    maximum.append(round(float(checking_value + (3 * sigma)), 2))
    minimum.append(round(float(checking_value - (3 * sigma)), 2))

frame = pd.DataFrame({'Date': date_index, 'Mean': checking_account,
                      'Maximum': maximum, 'Minimum': minimum})
frame.to_csv('../Input_Files/Checking.csv', index=False)
# eof
