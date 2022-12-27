#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 27 14:26:10 2022

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
pd.options.display.float_format = '{:.5f}'.format

import datetime
import pandas as pd
from dateutil.relativedelta import relativedelta
import locale
locale.setlocale(locale.LC_ALL, '')

"""
Example- Duration of a Bond

Consider a bond with issue date of 09-15-2022 with maturity date 09-15-2028 
at valuation date 02-21-2022. The coupon rate is 0.33% paid annually. The market
price is 98.75, Act/360. We have 7 cashflows where the last includes the face value.
We can solve, using Newton-Raphson or similar, the yield-to-maturity, ytm by:
    
    98.75 = 100/(1+ytm)^T + sum_of(n1 to T)[0.33/(1`+ ytm)^ti]

Details:
    marketPrice = 98.75
    T = 7
    parValue = 100
    annualCashFlow = 0.33/100
    valuationDate = 02-21-2022
    issueDate = 09-15-2022
    maturityDate = 09-15-2028
    ytm = unkown
"""

valuationDate = datetime.date(2022, 2, 21)
issueDate = datetime.date(2021, 9, 15)
maturityDate = datetime.date(2028, 9, 15)
marketPrice = 98.75
T = 7
parValue = 100
annualCashFlow = 0.33
dayCountBase=360

paymentDates = []
for x in range(T+1):
    paymentDates.append(issueDate + relativedelta(years=x))

paymentDateDF = pd.DataFrame()
paymentDateDF["Maturities"] = paymentDates


def getMaturityDates():
    maturitiesInDays = []
    paymentsToUse = paymentDates[1:]
    for y in range(len(paymentsToUse)):
        temp = (paymentsToUse[y] - valuationDate).days
        maturitiesInDays.append(temp)
    return maturitiesInDays

maturityInDays = getMaturityDates()

#print(maturityInDays)


#Calculate the discount ytms
def discountRates(rate):
    discYtm=[]
    for x in range(len(maturityInDays)):
        result = 1/(1+ (rate * maturityInDays[x]/dayCountBase))
        discYtm.append(result)
        result=0.0
    return discYtm


#Calculate the value of the fixed rate bonds
def fixedBondValues(rate):
    discYtm = discountRates(rate)
    values=[]
    for x in range(len(discYtm)):
        if x == len(discYtm) - 1:
            result = discYtm[x] * (0.33+100)
        elif x < len(discYtm) - 1:
            result = discYtm[x] * (0.33)
        values.append(result)
        result=0.0
    return values



def optimizationFunc(unkNownDiscFactor):
    a = marketPrice
    b = sum(fixedBondValues(unkNownDiscFactor))
    
    return b - a

solutions = fsolve(optimizationFunc, [0.2], xtol=1.49012e-08,)
spreadtoUse = solutions[0]
#print(spreadtoUse)



instrumentTable = pd.DataFrame()
instrumentTable["Dates"] = paymentDates[1:]
instrumentTable["CashFlows"] = [0.33, 0.33, 0.33, 0.33, 0.33, 0.33, 100.33]
instrumentTable["Days"] = maturityInDays
instrumentTable["DiscYTM"] = discountRates(spreadtoUse)
instrumentTable["Values"] = fixedBondValues(spreadtoUse)
instrumentTable["Value*Time"] = instrumentTable["Values"]*instrumentTable["Days"]/360

duration=sum((instrumentTable["Days"]/360)*instrumentTable["Values"])/marketPrice
MDuration = duration/(1+spreadtoUse)
DDuration = MDuration * marketPrice/100

duration2=sum(instrumentTable["Value*Time"])/marketPrice
# print(duration2)
# print()
#print()

print()
print("Duration of a Fixed-Rate Bond")
print()
print(f"Duration: {duration}")
print()
print(f"Modified Duration: {MDuration}")
print()
print(f"Dollar Duration: {DDuration}")
print()
print(instrumentTable)
