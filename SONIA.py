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
Date: 20221004	

Tenor        Maturity           Rate
SONIA1M	     1 Month            2.2420%
SONIA3M      3 Months           3.1273%	
SONIA6M      6 Months           3.9070%	
SONIA12M     12 Months          4.6759%
					
"""

#DECLARE SONIA AND OTHER VARIABLE INFORMATION HERE


val_date = datetime.date(2022, 10, 4)
tenor = [ "SONIA3M", "SONIA6M", "SONIA12M" ]
rate = [3.1273,3.9070,4.6759] #in percentage
dailyMaturities = []
monthlyMaturities = [3, 6, 12]
lenOfMaturity = len(rate)
lenOfMaturityPlusValueDate = len(rate) + 1
numberOfDays=0
result=0.0
dayCountBase = 360
SONIA = []
valuationDate = datetime.date(2022, 10, 4)

paymentDates = []
for x in [3, 6, 9]:
    paymentDates.append(valuationDate + relativedelta(months=x))

paymentDateDF = pd.DataFrame()
paymentDateDF["Maturities"] = paymentDates


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

instrumentTable, instrumentTable["Tenor"],instrumentTable["DateRateObserved"] = pd.DataFrame(), tenor,[valuationDate]*3
instrumentTable["observedRates"] = rate
instrumentTable["Maturities"] = maturities
instrumentTable["maturityInDays"] = maturityInDays


#Calculate the discount rate for SONIA
def discountSONIA():
    SONIA=[]
    for x in range(len(maturityInDays)):
        numberOfDays = (maturities[x] - val_date).days
        result = 1/(1+ (rate[x]/100.0 * numberOfDays/dayCountBase))
        SONIA.append(result)
        result=0.0
    return SONIA

SONIA = discountSONIA()
instrumentTable["discountRates"] = SONIA

#Function to calculate the implied forward rate
def impliedForwardRate():
    fRate = []
    result = 0.0
    for x in range(0,len(rate),1):
        if x == 0:
            fRate.append(rate[0]/100.0)
        elif x > 0:
            numberOfDays = (maturities[x] - maturities[x-1]).days
            result = ((SONIA[x-1]/SONIA[x]) - 1) * (1/(numberOfDays/360.0))
            
            fRate.append(result)
            result = 0.0
    fRate = [ x * 100 for x in fRate]
    return fRate
    
fRate = copy.deepcopy(impliedForwardRate())
instrumentTable["forwardRates"] = fRate

#To Display Rates - Original SONIA, Discount Rates and Implied Forward Rates
def ratePrinter():
    print("")
    print("SONIA ORIGINAL RATE, DISCOUNT RATE AND  IMPLIED FORWARD RATE")
    print("__________________________________________________________________")
    print("")
    print(instrumentTable.to_string())
    
ratePrinter()

"""
SONIA ORIGINAL RATE, DISCOUNT RATE AND  IMPLIED FORWARD RATE
__________________________________________________________________

      Tenor DateRateObserved  observedRates  Maturities  maturityInDays  discountRates  forwardRates
0   SONIA1M       2022-10-04         2.2420  2022-11-04              31       0.998073      2.242000
1   SONIA3M       2022-10-04         3.1273  2023-01-04              92       0.992071      3.570314
2   SONIA6M       2022-10-04         3.9070  2023-04-04             182       0.980631      4.666730
3  SONIA12M       2022-10-04         4.6759  2023-10-04             365       0.954737      5.335217
"""

print()
print()
CombDF = pd.merge(paymentDateDF, instrumentTable, on="Maturities", how='outer')
CombDF = CombDF.sort_values('Maturities', ascending=True)

CombDF["DateRateObserved"] = [val_date] * 4
CombDF["Type"] = ["Observed", "Observed",  "Interpolated","Observed" ]
CombDF["Tenor"] = [ "SONIA3M", "SONIA6M", "SONIA9M","SONIA12M" ]
newPaymentDates = []
for x in range(len(CombDF)):
    if x == 0:
        newPaymentDates.append((valuationDate + relativedelta(months=3)-valuationDate).days)
    elif x == 1:
        newPaymentDates.append((valuationDate + relativedelta(months=6)-valuationDate).days)
    elif x == 2:
        newPaymentDates.append((valuationDate + relativedelta(months=9)-valuationDate).days)
    elif x == 3:
        newPaymentDates.append((valuationDate + relativedelta(months=12)-valuationDate).days)
    
        
CombDF["maturityInDays"] = newPaymentDates
CombDF = CombDF.interpolate()

CombDF = CombDF[['Maturities',  'Type','Tenor', 'DateRateObserved', 'observedRates', 'maturityInDays', 'discountRates', 'forwardRates']]



CombDF["Exp"] = [[0,3],[3,6],[6,9],[9,12]]

print(CombDF)


def floatingRateDiscValueCalculator(CombDF):
    impliedForwardRate = CombDF["forwardRates"].tolist()
    discountRate = CombDF["discountRates"].tolist()
    maturityInDays = CombDF["maturityInDays"].tolist()
    res = []
    for x in range(len(maturityInDays)):
        if x == 0:
            temp = maturityInDays[x]/360 * impliedForwardRate[x] * discountRate[x]
            res.append(temp)
        elif x > 0:
            temp = (maturityInDays[x]-maturityInDays[x-1])/360 * impliedForwardRate[x] * discountRate[x]
            res.append(temp)
    return res

def FixedeDiscValueCalculator(r):
    fixedRate = r
    discountRate = CombDF["discountRates"].tolist()
    maturityInDays = CombDF["maturityInDays"].tolist()
    res = []
    for x in range(len(maturityInDays)):
        if x == 0:
            temp = maturityInDays[x]/360 * fixedRate * discountRate[x]
            res.append(temp)
        elif x > 0:
            temp = (maturityInDays[x]-maturityInDays[x-1])/360 * fixedRate * discountRate[x]
            res.append(temp)
    return res


def calCoupDiscFactors(CombDF):
    def optimizationFunc(r):
        a = sum(FixedeDiscValueCalculator(r))
        b = sum(floatingRateDiscValueCalculator(CombDF))
        return b - a
    solutions = fsolve(optimizationFunc, [0.9/100], xtol=1.49012e-08,)
    spreadtoUse = solutions[0]
       
        
    return spreadtoUse

fixedRate = calCoupDiscFactors(CombDF)  
print(fixedRate)       

discountFixedCashFlows = FixedeDiscValueCalculator(fixedRate)

print()
print(f"The Fixed Rate on the Swap is  {fixedRate}")
print()
discountFloatingCashFlows = floatingRateDiscValueCalculator(CombDF)

CombDF["DiscFixedCashFlows"] = discountFixedCashFlows
CombDF["DiscFloatingCashFlows"] = discountFloatingCashFlows

print()
print(CombDF)

print()
print()
print("Comparison of the Present Values of Fixed and Floating Legs:")
print()
sumOfFixedCashFlowPayments = sum(discountFixedCashFlows)

sumOfFloatingCashFlowPayments = sum(discountFloatingCashFlows)

print(f"Fixed Leg Total Discounted Value: {sumOfFixedCashFlowPayments}")
print()
print(f"Floating Leg Total Discounted Value: {sumOfFloatingCashFlowPayments}")


"""

The Fixed Rate on the Swap is  4.519428386374305

   Maturities          Type     Tenor DateRateObserved  observedRates  maturityInDays  discountRates  forwardRates      Exp  DiscFixedCashFlows  DiscFloatingCashFlows
0  2023-01-04      Observed   SONIA3M       2022-10-04        3.12730              92       0.992071      3.127300   [0, 3]            1.145808               0.792862
1  2023-04-04      Observed   SONIA6M       2022-10-04        3.90700             182       0.980631      4.666730   [3, 6]            1.107972               1.144085
2  2023-07-04  Interpolated   SONIA9M       2022-10-04        4.29145             273       0.967684      5.000974   [6, 9]            1.105493               1.223283
3  2023-10-04      Observed  SONIA12M       2022-10-04        4.67590             365       0.954737      5.335217  [9, 12]            1.102688               1.301731


Comparison of the Present Values of Fixed and Floating Legs:

Fixed Leg Total Discounted Value: 4.4619612922455785

Floating Leg Total Discounted Value: 4.4619612922455785
"""










