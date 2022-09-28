#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 17:11:55 2022

@author: oluwaseyiawoga
"""


from datetime import date
from dateutil.relativedelta import relativedelta
import copy
from numpy import array
import numpy as np
from scipy.optimize import fsolve
import pandas as pd
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

import datetime
import pandas as pd
from dateutil.relativedelta import relativedelta
import locale
locale.setlocale(locale.LC_ALL, '')

"""
Date: 20220927	

Tenor        Maturity           Rate
BSBYON       1 Day              3.10398%
BSBY1M	     1 Months           3.10835%
BSBY3M       3 Months           3.59024%	
BSBY6M       6 Months           4.22024%	
BSBY12M      12 Months          4.82726%
					
"""

#DECLARE BSBY AND OTHER VARIABLE INFORMATION HERE


val_date = datetime.date(2022, 9, 27)
tenor = ["BSBYON", "BSBY1M", "BSBY3M", "BSBY6M", "BSBY12M" ]
rate = [3.10398,3.10835,3.59024,4.22024,4.82726] #in percentage
dailyMaturities = [1]
monthlyMaturities = [1, 3, 6, 12]
lenOfMaturity = len(rate)
lenOfMaturityPlusValueDate = len(rate) + 1
numberOfDays=0
result=0.0
dayCountBase = 360
BSBY = []
valuationDate = datetime.date(2022, 9, 27)

def getMaturityDates():
    maturities = []
    maturitiesInDays = []
    for x in range(len(dailyMaturities)):
        temp = valuationDate + relativedelta(days=+dailyMaturities[x])
        temp_2 = (temp - valuationDate).days
        maturities.append(temp)
        maturitiesInDays.append(temp_2)
    for y in range(len(monthlyMaturities)):
        temp = valuationDate + relativedelta(months=+monthlyMaturities[y])
        temp_2 = (temp - valuationDate).days
        maturities.append(temp)
        maturitiesInDays.append(temp_2)
    return (maturities, maturitiesInDays)


maturities, maturityInDays = getMaturityDates()

instrumentTable, instrumentTable["Tenor"],instrumentTable["DateRateObserved"] = pd.DataFrame(), tenor,[valuationDate]*5
instrumentTable["observedRates"] = rate
instrumentTable["Maturities"] = maturities
instrumentTable["maturityInDays"] = maturityInDays


#Calculate the discount rate for BSBY
def discountBSBY():
    BSBY=[]
    for x in range(len(maturityInDays)):
        numberOfDays = (maturities[x] - val_date).days
        result = 1/(1+ (rate[x]/100.0 * numberOfDays/dayCountBase))
        BSBY.append(result)
        result=0.0
    return BSBY

BSBY = discountBSBY()
instrumentTable["discountRates"] = BSBY

#Function to calculate the implied forward rate
def impliedForwardRate():
    fRate = []
    result = 0.0
    for x in range(0,len(rate),1):
        if x == 0:
            fRate.append(rate[0]/100.0)
        elif x > 0:
            numberOfDays = (maturities[x] - maturities[x-1]).days
            result = ((BSBY[x-1]/BSBY[x]) - 1) * (1/(numberOfDays/360.0))
            
            fRate.append(result)
            result = 0.0
    fRate = [ x * 100 for x in fRate]
    return fRate
    
fRate = copy.deepcopy(impliedForwardRate())
instrumentTable["forwardRates"] = fRate

#To Display Rates - Original BSBY, Discount Rates and Implied Forward Rates
def ratePrinter():
    print("")
    print("BSBY ORIGINAL RATE, DISCOUNT RATE AND  IMPLIED FORWARD RATE")
    print("__________________________________________________________________")
    print("")
    print(instrumentTable.to_string())
    
ratePrinter()

"""
BSBY ORIGINAL RATE, DISCOUNT RATE AND  IMPLIED FORWARD RATE
__________________________________________________________________

     Tenor DateRateObserved  observedRates  Maturities  maturityInDays  discountRates  forwardRates
0   BSBYON       2022-09-27        3.10398  2022-09-28               1       0.999914      3.103980
1   BSBY1M       2022-09-27        3.10835  2022-10-27              30       0.997416      3.108233
2   BSBY3M       2022-09-27        3.59024  2022-12-27              91       0.991006      3.817347
3   BSBY6M       2022-09-27        4.22024  2023-03-27             181       0.979222      4.813555
4  BSBY12M       2022-09-27        4.82726  2023-09-27             365       0.953341      5.311677
"""
