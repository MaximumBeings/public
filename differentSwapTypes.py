#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 10:39:59 2023

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
pd.options.display.float_format = '{:.2f}'.format

import datetime
import pandas as pd
from dateutil.relativedelta import relativedelta
import locale
locale.setlocale(locale.LC_ALL, '')


"""
PRICING A 5-YEAR SEMI-ANNUAL AMORTIZING INTEREST RATE SWAPS

The pricing of an interest rate swap involves finding the fixed-rate  for the swap. 
Conventionally, the notional of an IRS stays constant over the life of the swap but 
how about if the notional does not stay the same but either accretes or
amortizes as we move towards maturity? These types of swaps are known as
accreting and amortizing swaps respectively. In order to price an interest
rate swap, it is necessary to perform the following steps:
    
    
    Step 1: Construct a cash curve
    
    Step 2: Derive a zero coupon curve
    
    Step 3: Calculate the discount factors to find present values
    
    Step 4: Derive an implied forward curve
    
    Step 5: Find the present value of the floating side of the swap.
    
    Step 6: Use numerical methods or optimization to find the fixed swap rate.
    
    Step 7: Equate the P.V. of the floating side, with the P.V of the fixed side
    and this find the value of the fixed rate.
    
    Day Count Convention:
        We have to count the actual number of days in a particular six-month period.
        Use actual/360 for U.S. $ floating rates and 180/360 for U.S. $ fixed rates. To
        keep it simple, we shall assume 180 days in a six-month period.
    
    Steps 1 and 2:
        It is assumed that you already have a zero coupon curve for 6 years at six-month
        intervals. Therefore, steps 1 and 2 are already completed.

    After Steps 1 and 2:
        
    Maturity(Six Months)     Annual(ZCR)      Semi-Annual(ZCR)
            1                   5.00%            2.50%
            2                   5.50%            2.75%
            3                   6.00%            3.00%
            4                   6.50%            3.25%
            5                   7.00%            3.50%
            6                   7.25%            3.625%
            7                   7.50%            3.75%
            8                   7.75%            3.875%
            9                   8.00%            4.00%
            10                  8.16%            4.08%
                           
        
"""

#Declare Variables:

period = [1,2,3,4,5,6,7,8,9,10]
zcr = [2.50, 2.75, 3.00,3.25,3.50,3.625,3.75,3.875,4.00,4.08]
notionalAmount= [50000000,50000000,40000000,40000000,30000000,30000000,20000000,20000000,10000000,10000000]
valuationDate = datetime.date(2023, 1, 22)



def calculateDiscountRate(period, zcr):
    """
    If y is the interest rate for the Nth period, the discount factor, namely the P.V.
    factor is:
        1/(1+y)^N
    """
    result = []
    for x in range(len(period)):
        result.append(1/((1+zcr[x]/100)**period[x]))
    return result




    

"""
Step 4: Derive implied Forward Rates
The following notation is used. Time 0 refers to today.

0F1 = Zero coupon spot rate for six months.
1F2 = Implied Forward Rate, starting one period from today. In this example, each
period is six months. Thus, 1F2 refers to six months forward rate starting six
months from today.

2F3 = Implied Forward Rate, starting two periods from today. Six month forward
rate starting one year from today.

3F4 = Implied Forward Rate, starting three periods from today. Six month forward
rate starting eighteen months from today.

Similar notation is used for all periods. The implied forward rates are calculated
as break-even rates; thus the concept of indifference between maturities is used.
( 1 + 0F1 ) ( 1 + 1F2 ) = ( 1 + 0F2 )**2
In this example, 0F1 = 2.5%
0F2 = 2.75%
1F2 has to be found
1 + 1F2 = ( 1 + 0F2 )2
( 1 + 0F1 )
= (1.0275)2
(1.025)
= 1.03001
1F2 = 3.001%
Using a similar procedure, all other forward rates are found.
"""

def impliedForwardRate(period, zcr):
    result = []
    temp=0.0
    for x in range(0,len(period)):
        if x == 0:
            result.append(zcr[0])
        elif x > 0:
            temp = ((1+zcr[x]/100)**period[x])/((1+zcr[x-1]/100)**period[x-1]) - 1
            result.append(temp*100)
    return result


    

def calcFloatingSide(instrumentTable):
    """
    Calculate the periodic cash flows and present value of Floating Side
    """
    instrumentTable["Floating"] = instrumentTable["Notional"] * (instrumentTable["Forward_Rate"]/100) * instrumentTable["Disc_Factor"]
    return instrumentTable




def calcFixedSide(fixedRate,instrumentTable):
    result = []
    for x in range(0,len(period)):
        temp = instrumentTable["Notional"][x] * (fixedRate/100) * instrumentTable["Disc_Factor"][x]
        result.append(temp)
    return result

def optimizationFunc(unkNownDiscFactor,instrumentTable):
        a = sum(instrumentTable["Floating"])
        b = sum(calcFixedSide(unkNownDiscFactor,instrumentTable))
        return b - a



def main(notional, typeOfInstrument):
    instrumentTable = pd.DataFrame()
    instrumentTable["Period"] = period
    instrumentTable["Zero_Coupon_Rate"] = zcr
    instrumentTable["Notional"] = notional
    pv = calculateDiscountRate(period, zcr)
    instrumentTable["Disc_Factor"] = pv
    impliedForwardRate_ = impliedForwardRate(period, zcr)
    instrumentTable["Forward_Rate"] = impliedForwardRate_
    instrumentTable=calcFloatingSide(instrumentTable)
    solutions = fsolve(optimizationFunc, [0.2], instrumentTable,xtol=1.49012e-08,)
    spreadtoUse = solutions[0]
    instrumentTable["Fixed"] = calcFixedSide(spreadtoUse,instrumentTable)
    return (spreadtoUse,instrumentTable,typeOfInstrument)



def tableGenerator(listOfListOfNotionals, listOfTypes):
    
    for x in range(len(listOfListOfNotionals)):
        spreadtoUse,instrumentTable, swapType= main(listOfListOfNotionals[x], listOfTypes[x])
        print()
        print(f"Hypothetical {swapType} Swap Pricing & Valuation - Dizzle Algorithms Inc")
        print("Fixed Income Research Department: Valuation & Duration of Interest Rate Swaps")
        print()
        print("Valuation Date:")
        print()
        print(valuationDate.strftime("%Y-%m-%d %I:%M:%S %p"))
        print()
        print(f"Swap Fixed Rate: {spreadtoUse}")
        print()
        print(f"Original Value of Fixed Rate Leg: {round(sum(instrumentTable['Fixed']),4)}")
        print()
        print(f"Original Value of Floating Rate Leg: {round(sum(instrumentTable['Floating']),4)}")
        print()
        print(f"Value of Swap: {round(sum(instrumentTable['Floating']) - sum(instrumentTable['Floating']),4)}")
        print()
        print(instrumentTable)

plainVanilla = [50000000,50000000,50000000,50000000,50000000,50000000,50000000,50000000,50000000,50000000]
amortizing = [50000000,50000000,40000000,40000000,30000000,30000000,20000000,20000000,10000000,10000000]
accreting = [10000000,10000000,20000000,20000000,30000000,30000000,40000000,40000000,50000000,50000000]
rollerCoaster = [50000000,50000000,10000000,10000000,30000000,30000000,20000000,20000000,10000000,50000000]

listOfListOfNotionals = [plainVanilla, amortizing, accreting, rollerCoaster]
listOfTypes = ["Plain Vanilla", "Amortizing", "Accreting", "Roller Coaster"]

tableGenerator(listOfListOfNotionals, listOfTypes)




