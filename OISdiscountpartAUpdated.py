# -*- coding: utf-8 -*-

"""

********************************************************************************************************
This is an update of an earlier program on the same topic to clean it up so that we can cover the second
part that uses OIS instead of LIBOR rates.  The original version was a rough prototype and this
one will be easier to update for the OIS version. Note that this example assumes that the
valuation date and payment date falls on the same date so we did not take into account accruals
between payment dates. We will do a version that covers accrual of interest rate between payment
dates.  See you next time!!
********************************************************************************************************


TITLE: Valuing Interest Rate Swaps Using OIS Discounting (Part A)

SOURCE: Boston University School of Management Research Paper Series (No.2012-­‐11)
Valuing Interest Rate Swaps Using OIS Discounting By Donald J. Smith
Electronic copy available at: http://ssrn.com/abstract=2036979


OBJECTIVE: Compare Swap Market Value using both LIBOR discounting and OIS discounting
and discuss the python implementation of the two methodologies using the
above article as the main source. In this part of the series we only discussed
swap valuation using LIBOR discounting. Subsequently, we will discuss the OIS
discounting methodology. To read about the relative merit of OIS discounting over
LIBOR discounting refer to the above article or other sources.


IMPLEMENTATION:

Consider a 2-year, USD 100,000,000.00 (100 million USD) notional principal,
5.26% fixed versus 3-month LIBOR, quarterly settlement swap at a time when the
otherwise comparable at-market fixed rate is 3.40%.

Time Description Rate
3-month LIBOR 0.50%
6-month LIBOR 1.00%
9-month LIBOR 1.60%
12-month LIBOR 2.10%
15-month SFR 2.44%
18-month SFR 2.76%
21-month SFR 3.08%
24-month SFR 3.40%

Valuation Date is March 15th 2010.

Typically, swap fixed rates start at a tenor of two years. This creates the need to
interpolate for the span between year one and year two. However, this example assumes
that the swap fixed for 15th, 18th and 21st month have already been boostrapped.

Date Count Convention -> Actual/360

"""

import datetime
import pandas as pd
from dateutil.relativedelta import relativedelta
import locale
locale.setlocale(locale.LC_ALL, '')

#Declare Variables
val_date = datetime.date(2010, 3, 15)
rate = [0.50,1.00,1.60,2.10,2.44,2.76,3.08,3.40] #in percentage
lenOfMaturity = len(rate)
lenOfMaturityPlusValueDate = len(rate) + 1
numberOfDays=0
result=0.0
dayCountBase = 360
LIBOR = []
fixedRate = 0.0526
notionalPrincipal = 100000000
SFRStartingIndex = 4
valuationDate = datetime.date(2010, 3, 15)
compounding = 3
 

#Generate a list of cashflow payment dates
def maturities(x,compounding):
    maturities = []
    for y in range(1,lenOfMaturityPlusValueDate):
        maturities.append((x)+relativedelta(months=compounding*y))
    return maturities
    
maturities = maturities(valuationDate,compounding)

#Calculate the discount rate for LIBOR
def discountLIBOR():
    for x in range(SFRStartingIndex):
        numberOfDays = (maturities[x] - val_date).days
        result = 1/(1+ (rate[x]/100.0 * numberOfDays/dayCountBase))
        LIBOR.append(result)
        result=0.0
    return LIBOR

#Helper function used in calculating the Swap Fixed Rate
def discountSFRhelper(LIBORlist,n):
    final = 0.0
    ans = 0.0
    for x in range(n):
        if x == 0:
            numberOfDays = (maturities[x] - val_date).days
            ans = numberOfDays/360.0 * LIBORlist[x]
            final = final + ans
            
        else:
            numberOfDays = (maturities[x] - maturities[x-1]).days
            ans = numberOfDays/360.0 * LIBORlist[x]
            final = final + ans       
    return final

#Another helper function - to help copy one list to another to avoid list mutation
#Source: StackOverFlow
def deepcopy(A):
    rt = []
    for elem in A:
        if isinstance(elem,list):
            rt.append(deepcopy(elem))
        else:
            rt.append(elem)
    return rt
    
#Function to calculate Swap Fixed Rate
def swapRateCalculator():
    final = 0.0
    ans = 0.0
    LIBOR = deepcopy(discountLIBOR())
    SFRRate = deepcopy(rate[SFRStartingIndex:])
    for x in range(SFRStartingIndex,lenOfMaturity):
        numberOfDays = (maturities[x] - maturities[x-1]).days
        ans = (1 - SFRRate[x-SFRStartingIndex]/100.0 * discountSFRhelper(LIBOR,x))
        final=ans/(1 + SFRRate[x-SFRStartingIndex]/100.0 * numberOfDays/360.0)
        LIBOR.append(final)
    return LIBOR
    

LIBOR = deepcopy(swapRateCalculator())  #Update LIBOR list by passing the result of swapRateCalculator function to a variable called LIBOR

#Functuion to calculate the implied forward rate
def impliedForwardRate():   
    fRate = []
    result = 0.0
    for x in range(0,lenOfMaturity,1):
        if x == 0:
            fRate.append(rate[0]/100.0)
        elif x > 0:
            numberOfDays = (maturities[x] - maturities[x-1]).days
            result = ((LIBOR[x-1]/LIBOR[x]) - 1) * (1/(numberOfDays/360.0))
            fRate.append(result)
            result = 0.0
    return fRate
    
fRate = deepcopy(impliedForwardRate())

#To Display Rates - Original LIBOR/Swap Fixed Rates, Discount Rates and Implied Forward Rates
def ratePrinter():
    print ""
    print "Original Rate, Discount Rate and Implied Forward Rate"
    print ""
    rateTable = pd.DataFrame.from_items([('Period', range(1,lenOfMaturityPlusValueDate,1)),('Rate', rate), ('Disc_Rate', LIBOR),('Imp_For_Rate', fRate)])
    print(rateTable.to_string())


#To Calculate the Market Value of Fixed Rate Note/Leg
def fixedRateLeg():
    result = 0.0
    ans = 0.0
    for x in range(0,lenOfMaturity,1):
        if x == 0:
            numberOfDays = (maturities[x] - val_date).days
            ans = ans + numberOfDays/360.0 * LIBOR[x]
        else:
            numberOfDays = (maturities[x] - maturities[x-1]).days
            ans = ans + numberOfDays/360.0 * LIBOR[x]
 
        result = ans *notionalPrincipal * fixedRate + notionalPrincipal * LIBOR[-1]
    return result
    
#To Calculate the Market Value of Floating Rate Note/Leg
#The market value of the floating rate is is assumed to reset to par
#at payment periods but can be recalculated as follow:

def floatingRateLeg():
    result = 0.0
    ans = 0.0
    for x in range(0,lenOfMaturity,1):
        if x == 0:
            numberOfDays = (maturities[x] - val_date).days
            ans = ans + LIBOR[x] * fRate[x] * numberOfDays/360.0
        else:
            numberOfDays = (maturities[x] - maturities[x-1]).days
            ans = ans + LIBOR[x] * fRate[x] * numberOfDays/360.0 
    result = notionalPrincipal * LIBOR[-1] + ans * notionalPrincipal
    return result
    
   
#To Calculate the Market Value of Swap = Market Value of Fixed Leg = Market Value of Floating Leg
def swapMarketValue():
    return fixedRateLeg() - floatingRateLeg()
    
    
#Sample Calls
ratePrinter()
print ""
print ("Market Value of Fixed Rate Leg = ") + str(locale.currency(fixedRateLeg(),grouping=True))
print ""
print ("Market Value of Floating Rate Leg = ") + str(locale.currency(floatingRateLeg(),grouping=True))
print ""
print ("Market Value of Swap: (MV Fixed - MV FRN) = ") + str(locale.currency(swapMarketValue(),grouping=True))

#Sample Ouptput
"""
Original Rate, Discount Rate and Implied Forward Rate

   Period  Rate  Disc_Rate  Imp_For_Rate
0       1  0.50   0.998724      0.005000
1       2  1.00   0.994915      0.014981
2       3  1.60   0.987925      0.027989
3       4  2.10   0.979152      0.035840
4       5  2.44   0.969457      0.039132
5       6  2.76   0.958690      0.043949
6       7  3.08   0.946531      0.050818
7       8  3.40   0.932957      0.057556

Market Value of Fixed Rate Leg = $103,667,623.63

Market Value of Floating Rate Leg = $100,000,000.00

Market Value of Swap: (MV Fixed - MV FRN) = $3,667,623.63

"""
