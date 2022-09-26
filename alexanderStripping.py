#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 25 19:00:04 2022

@author: oluwaseyiawoga
"""
from datetime import date
from dateutil.relativedelta import relativedelta

from numpy import array
import numpy as np
from scipy.optimize import fsolve
import pandas as pd
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

"""
BootStrapping
Source: Carol Alexander -> Pricing, Hedging and Trading Financial Instruments.
Example III.I.21 Coupon Stripping

Calculate the zero coupon rates from the market prices of four zero coupon bonds 
and two coupon bearing bonds shown in the table below:
    Maturity    Coupon    Market_Price
    1 Month     0         99.5
    2 Months    0         99.1
    3 Months    0         98.7
    4 1 Year    0         95.0
    5 2 Years   6%        101.0
    6 3 Years   10%       112.0
    
Start_Date: Today
"""

monthlyMaturities = [1, 2, 3]
coupons = [0, 0, 0, 0, 0.06, 0.10]
mktValues = [99.5, 99.1, 98.7, 95.0, 101.0, 112.0]
bond_types = ["Zero", "Zero", "Zero", "Zero", "Coupon", "Coupon"]
yearlyMaturities = [1, 2, 3]
matInYears = [None, None, None, 1, 2, 3]
matInMonths = [1, 2, 3, None, None, None]

startDate = date.today()


def getMaturityDates():
    maturities = []
    maturitiesInDays = []
    for x in range(len(monthlyMaturities)):
        temp = startDate + relativedelta(months=+monthlyMaturities[x])
        temp_2 = (temp - startDate).days
        maturities.append(temp)
        maturitiesInDays.append(temp_2)
    for y in range(len(yearlyMaturities)):
        temp = startDate + relativedelta(years=+yearlyMaturities[y])
        temp_2 = (temp - startDate).days
        maturities.append(temp)
        maturitiesInDays.append(temp_2)
    return (maturities, maturitiesInDays)


maturity, maturityInDays = getMaturityDates()

instrumentTable = pd.DataFrame()
instrumentTable["Types"] = bond_types
instrumentTable["Coupon"] = [0, 0, 0, 0, 0.06, 0.10]
instrumentTable["Market_Value"] = mktValues
instrumentTable["Maturities"] = maturity
instrumentTable["maturityInDays"] = maturityInDays
instrumentTable["Monthly"] = matInMonths
instrumentTable["Yearly"] = matInYears
# print(instrumentTable)

"""
    Types  Coupon  Market_Value  Maturities  maturityInDays  Monthly  Yearly
0    Zero    0.00          99.5  2022-10-26              30      1.0     NaN
1    Zero    0.00          99.1  2022-11-26              61      2.0     NaN
2    Zero    0.00          98.7  2022-12-26              91      3.0     NaN
3    Zero    0.00          95.0  2023-09-26             365      NaN     1.0
4  Coupon    0.06         101.0  2024-09-26             731      NaN     2.0
5  Coupon    0.10         112.0  2025-09-26            1096      NaN     3.0
"""


def calcZeroCoupDiscFactors(instrumentTable):
    res = []
    for x in range(len(instrumentTable)):
        tempInfo = instrumentTable.iloc[x]
        if tempInfo.Types == 'Zero':
            res.append(tempInfo.Market_Value/100)
        else:
            res.append(None)
    instrumentTable["DiscFactor"] = res
    return instrumentTable

instrumentTable = calcZeroCoupDiscFactors(instrumentTable)

def calCoupDiscFactors(instrumentTable):
    issuePrice = 0

    def calcDiscount(unkNownDiscFactor):
        temp = 0
        for x in range(len(knownDiscFactors)):
            temp = temp + knownDiscFactors[x] * (coupon*100)
        temp = temp + ((100+(coupon*100))*unkNownDiscFactor)
        return temp

    def optimizationFunc(unkNownDiscFactor):
        a = issuePrice
        b = calcDiscount(unkNownDiscFactor)
        return b - a
    countZeroCouponBonds = 0
    for x in range(len(instrumentTable)):
        tempInfo = instrumentTable.iloc[x]
        if tempInfo.Types != 'Coupon':
            countZeroCouponBonds = countZeroCouponBonds + 1

    for x in range(len(instrumentTable)):
        tempInfo = instrumentTable.iloc[x]
        if tempInfo.Types == 'Coupon':
            noOfYears = int(tempInfo.Yearly)
            coupon = tempInfo.Coupon
            issuePrice = tempInfo.Market_Value
            knownDiscFactors = list(instrumentTable["DiscFactor"][countZeroCouponBonds-1:x])
            solutions = fsolve(optimizationFunc, [0.9/100], xtol=1.49012e-08,)
            spreadtoUse = solutions[0]
            update = list(instrumentTable['DiscFactor'])
            update[x]= spreadtoUse
            instrumentTable['DiscFactor'] = update
            
    return instrumentTable

instrumentTable = calCoupDiscFactors(instrumentTable)  
print(instrumentTable)       
"""
    Types  Coupon  Market_Value  Maturities  maturityInDays  Monthly  Yearly  DiscFactor
0    Zero    0.00          99.5  2022-10-26              30      1.0     NaN    0.995000
1    Zero    0.00          99.1  2022-11-26              61      2.0     NaN    0.991000
2    Zero    0.00          98.7  2022-12-26              91      3.0     NaN    0.987000
3    Zero    0.00          95.0  2023-09-26             365      NaN     1.0    0.950000
4  Coupon    0.06         101.0  2024-09-26             731      NaN     2.0    0.899057
5  Coupon    0.10         112.0  2025-09-26            1096      NaN     3.0    0.850086
"""
