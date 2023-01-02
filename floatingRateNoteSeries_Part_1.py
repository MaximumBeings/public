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
PROBLEM -> Valuation of the Floating Rate Leg of an Interest Rate Swap Versus 
            Valuation of a Floating Rate Note (FRN) (Part 1 of 10)
            
    Consider an interest rate swap that was issued on 12/29/2022 to pay fixed
    and receive floating on a quarterly basis for 50 years. The underlying benchmark 
    reference rate for this instrument is the UK's Government Bond and Gilts rates as shown
    below. Calculate the value of the floating rate leg of the instrument and implement it in Python.
    For periods for which the rates are not directly observable, use interpolation techniques to
    fill the curve.
    
    
    
Residual_Maturity       Rate         ZC_Price
3 months                3.345%
6 months                4.015%
1 year                  3.423%        96.69
2 years                 3.593%        93.18
3 years                 3.552%        90.06
4 years                 3.659%        86.61
5 years                 3.651%        83.59
6 years                 3.650%        80.65
7 years                 3.717%        77.46
8 years                 3.644%        75.10
9 years                 3.706%        72.07
10 years                3.693%        69.58
12 years                3.879%        63.34
15 years                4.018%        55.39
20 years                4.064%        45.08
25 years                4.049%        37.07
30 years                3.980%        31.01
40 years                3.626%        24.06
50 years                3.590%        17.14

Source: http://www.worldgovernmentbonds.com/country/united-kingdom/
Date: 20221229	
  				
"""

#DECLARE VARIABLE INFORMATION HERE
"""
***PROTOTYPE:
For the purpose of constructing our interest rate input data, we start from the rates at 3 months.
This is because the underlying swaps pay interests on quarterly basis. We ignore interest rate reset
dates and assume that the interest rates were observed on the valuation date which coincides with the 
issuance date. This was done to establish a base case. In a future version we will consider scenarios
where the calculation dates occur at a timeperiod after the initial issuance. As you are already aware
the observed rate are only available at commonly quoted intervals, hence, interpolation was necessary to 
generate rates for the payment periods for which rates were not observable. Linear interpolation was used
in this case but it could have been configured to use any interpolation scheme.

In order to determine the fixed rate, on the fixed payer leg, optimization was used to determine the rate that
sets the fixed coupon payment equalt to the discounted value of the floating legs.

The underlying rate on the interest rate swap is the gilt edge (UK), though this can be reconfigured to use any benchmark
interest rate and  the maturity is for 50 years ona plain-vanilla fixed for floating interest rate swap. Exchange of cashflows
occur on a quarterly basis for both fixed and floating leg.

In a future iteration, we will consider a scenario where calculation occurred after issuance and explore other benchmark
interest rates namely SOFR, EURIBOR, SONIA, SEK, US Treasury rates etc.
TODOS:
    Modified Duration including Bloomberg Methodology
    OIS Discounting Methodology
    Floating Rate Note (Not floating rate leg of an interest rate swap)
    Potentially reconfigure to use Object Oriented Programming and implement different constructors to handle different cases
    Unit Testing and potentially rebuild in Excel for testing purposes.
    Potentially inculcate day count conventions and test by using other methods to calculate forward rates (two other methods)
    Expand to other types of instruments and securities
    
Sources: Duration Measure -> Jan Roman
         Muzi Mavuso (2012). Money Market SubCommittee (MMS) - Floating Rate Note Speci cations Johannesburg, South Africa.
         Bond Math -> Donald Smith
         Pricing Hedging and Other Derivatives -> Carol Alexander
         Options, Futures & Other Derivatives -> John Hull
         Valuation of Floating Rate Notes -> Oluwaseyi Awoga
         https://en.wikipedia.org/wiki/Forward_rate
         
Data Source:
    Source: http://www.worldgovernmentbonds.com/country/united-kingdom/
"""

#Declare initial valiables and input data
val_date = datetime.date(2022, 12, 29)
valuationDate = datetime.date(2022, 12, 29)
dailyMaturities = []
monthlyMaturities = [ 3, 6]
yearlyyMaturities = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15, 20, 25, 30, 40, 50]
rates = [3.345, 4.015, 3.423, 3.593, 3.552, 3.659, 3.651, 3.650, 3.717, 3.644, 3.706, 3.693, 3.879, 4.018, 4.064, 4.049, 3.980, 3.626, 3.590]
ZeroCoupon = ["N/A", "N/A", 96.69, 93.18, 90.06, 86.61,83.59, 80.65, 77.46, 75.10,  72.07, 69.58, 63.34,55.39, 45.08, 37.07, 31.01,24.06, 17.14  ]
numberOfDays=0
result=0.0
dayCountBase = 365  #Assumed
GILT = []
finalMaturityDate = val_date + relativedelta(years=50)
numberOfPaymentPeriod = (finalMaturityDate - val_date).days/92
numberOfPaymentPeriod = int(round(numberOfPaymentPeriod,-2))



def generatePaymentDates():
    """
    This function generates the interest payment dates
    """
    paymentDates = []
    for x in range(1, numberOfPaymentPeriod+1):
        paymentDates.append(valuationDate + relativedelta(months=x*3))
    
    paymentDateDF = pd.DataFrame()
    paymentDateDF["Maturities"] = paymentDates
    return (paymentDateDF,paymentDates)
    
paymentDateDF,paymentDates = generatePaymentDates()


def getMaturityDates():
    """
    This function generates the maturities of the interest rates and the maturity in days
    """
    maturities = []
    maturitiesInDays = []
    for x in range(len(monthlyMaturities)):
        temp = valuationDate + relativedelta(months=+monthlyMaturities[x])
        temp_2 = (temp - valuationDate).days
        maturities.append(temp)
        maturitiesInDays.append(temp_2)
    for y in range(len(yearlyyMaturities)):
        temp = valuationDate + relativedelta(years=+yearlyyMaturities[y])
        temp_2 = (temp - valuationDate).days
        maturities.append(temp)
        maturitiesInDays.append(temp_2)
    return (maturities, maturitiesInDays)

maturities, maturitiesInDays = getMaturityDates()

#Calculate the discount rate for rates
def discountRATES_2(rates):
    RATES=[]
    for x in range(len(maturitiesInDays)):
        numberOfDays = (maturities[x] - val_date).days
        result = 1/((1+ (rates[x]/100.0))** (numberOfDays/365))
        RATES.append(result)
        result=0.0
    return RATES

discRates = discountRATES_2(rates)


#Function to calculate the implied forward rate
def impliedForwardRate(observedRates, RATES):
    """
    Source: https://en.wikipedia.org/wiki/Forward_rate
    The forward rate can be expressed in terms of discount factors 
    FWDrate1,2 = 1/(t2-t1) * (DF(0,t1)/DF(0,t2) - 1)
    """
    fRate = []
    result = 0.0
    for x in range(0,len(RATES),1):
        if x == 0:
            fRate.append(observedRates[0]/100.0)
        elif x > 0:
            numberOfDays = (maturities[x] - maturities[x-1]).days
            result = ((RATES[x-1]/RATES[x]) - 1) * (1/(numberOfDays/360.0))
            
            fRate.append(result)
            result = 0.0
    fRate = [ x * 100 for x in fRate]
    return fRate
    
impliedForWardRates = impliedForwardRate(rates, discRates)


def generateInstrumentTable():
    """
    This function generates an intermediate table used in the process
    """
    instrumentsTable = pd.DataFrame()
    instrumentsTable["Start_Date"] = [valuationDate]*len(maturities)
    instrumentsTable["Maturities"] = maturities
    instrumentsTable["Days"] = maturitiesInDays
    instrumentsTable["Rates"] = rates
    instrumentsTable["Obs_Zero_Coupon"] = ZeroCoupon
    instrumentsTable["DiscountFactors"] = [d * 100 for d in discRates]
    instrumentsTable["implied_Forward_Rate"] = impliedForWardRates
    return instrumentsTable

instrumentsTable = generateInstrumentTable()


def generateCompleteTable():
    """
    This function generates and aggregates relevant data points
    NOTE: Interpolation occurred here.
    """
    NoOfInterestPaymentDays = []
    toUse = paymentDates
    for d in range(len(toUse)):
        if d == 0:
            NoOfInterestPaymentDays.append(90)
        elif d > 0:
            temp2 = (toUse[d]-toUse[d-1]).days
            NoOfInterestPaymentDays.append(int(temp2))
    
    
    completeTable = paymentDateDF.merge(instrumentsTable, on='Maturities', how='left', suffixes=('_1', '_2'))
    completeTable["Maturities"] = paymentDates
    completeTable['Rates'].interpolate(inplace=True)
    completeTable['DiscountFactors'].interpolate(inplace=True)
    completeTable['implied_Forward_Rate'].interpolate(inplace=True)
    completeTable['Days'].interpolate(inplace=True)
    completeTable['NoOfInterestPaymentDays'] = NoOfInterestPaymentDays
    completeTable['NoOfInterestPaymentDays'].interpolate(inplace=True)
    completeTable['Start_Date'] = [completeTable['Start_Date'][0]] * len(completeTable)
    completeTable = completeTable[['Maturities', 'Start_Date', 'Days','NoOfInterestPaymentDays', 'Rates', 'Obs_Zero_Coupon', 'DiscountFactors', 'implied_Forward_Rate', ]]
    completeTable = completeTable[['Start_Date', 'Maturities','Days', 'NoOfInterestPaymentDays','Rates', 'DiscountFactors', 'implied_Forward_Rate', ]]
    completeTable['Days'] = completeTable['Days'].astype(int)
    completeTable['NoOfInterestPaymentDays'] = completeTable['NoOfInterestPaymentDays'].astype(int)
    projections = []
    a = 0
    b = 3
    for g in range(len(completeTable)):
        projections.append([a,b])
        a = a + 3
        b = b + 3 
    
    completeTable["FwdRateProjections"] = projections
    return completeTable
    

completeTable = generateCompleteTable()

        
def floatingRateDiscVal(completeTable):
    """
    This function calculates the discounted value of the floating rate leg
    """
    impliedForwardRate = completeTable['implied_Forward_Rate'].tolist()
    discountRate = completeTable['DiscountFactors'].tolist()
    maturityInDays = completeTable['Days'].tolist()
    
    res = []
    for x in range(len(maturityInDays)):
        if x == 0:
            temp = (maturityInDays[x]/365 * impliedForwardRate[x]/100.00 * discountRate[x]/100.00)*100.00
            res.append(temp)
        elif x > 0:
            temp = ((maturityInDays[x]-maturityInDays[x-1])/365 * impliedForwardRate[x]/100.00 * discountRate[x]/100)*100.00
            res.append(temp)
    return res



#Calculate the value of the fixed rate bonds
def fixedBondValues(unknownRate):
    """
    This function calculates the discounted value of the fixed rate leg
    """
    discountRate = completeTable['DiscountFactors'].tolist()
    maturityInDays = completeTable['Days'].tolist()
    values=[]
    for x in range(len(discountRate)):
        if x == 0:
            result = discountRate[x]/100.00 * 90/365 * unknownRate
        elif x > 0:
            result = discountRate[x]/100.00 * (maturityInDays[x]-maturityInDays[x-1])/365 * unknownRate
        values.append(result)
        result=0.0
    return values




def generateFinalOutput():
    """
    This function generates the final output and uses optimization to generate the fixed rate
    """
    discountedValue = floatingRateDiscVal(completeTable)
    completeTable["Floating_Values"] = discountedValue
    def optimizationFunc(unkNownDiscFactor):
        a = sum(completeTable["Floating_Values"])
        b = sum(fixedBondValues(unkNownDiscFactor))
        return b - a
    solutions = fsolve(optimizationFunc, [0.2], xtol=1.49012e-08,)
    spreadtoUse = solutions[0]
    fixedLegValues = fixedBondValues(spreadtoUse)
    completeTable["Fixed_Values"] = fixedLegValues
    completeTable["Swap Values"] =  completeTable["Fixed_Values"] + completeTable["Floating_Values"]
    
    return completeTable

completeTable = generateFinalOutput()
    
   
def finalResultPrintOut(): 
    
    print()
    print("Observed UK Gilts & Government Bond Rates (50 Years Maturity) - Dizzle Algorithms Inc")
    print("Valuation of the Floating Rate Leg of an Interest Rate Swap Versus Valuation of a Floating Rate Note (FRN) (Part 1 of 10)")
    print("Source: http://www.worldgovernmentbonds.com/country/united-kingdom/")
    print()
    print("Valuation Date:")
    print(valuationDate.strftime("%Y-%m-%d %I:%M:%S %p"))
    
    print()
    print("Value of Floating Leg of an InterestRate Swap:")
    print()
    a = sum(completeTable["Fixed_Values"])
    print(f"Value of Fixed Rate Leg: {a}")
    print()
    b = sum(completeTable["Floating_Values"])
    print(f"Value of Floating Rate Leg: {b}")
    print()
    c = a + b
    print(f"Total Value : {c}")
    print()
    print(completeTable.to_string(index=False))


finalResultPrintOut()








