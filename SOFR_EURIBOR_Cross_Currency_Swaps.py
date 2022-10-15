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
Date: 20221013	

Tenor        Maturity           Rate
SOFR1M	     1 Month            3.37566%
SOFR3M       3 Months           3.86361%	
SOFR6M       6 Months           4.23993%	
SOFR12M      12 Months          4.47309%
					
"""

"""
Date: 20221013	

Tenor            Maturity           Rate
EURIBOR1W	     1 Week             0.6280%
EURIBOR1M	     1 Month            0.8450%
EURIBOR3M        3 Months           1.3780%	
EURIBOR6M        6 Months           2.0120%	
EURIBOR12M       12 Months          2.6610%
					
"""

"""
Thursday 13 October 2022	1 EUR = 0.97782 USD
"""

#DECLARE SOFR & EURIBOR AND OTHER VARIABLE INFORMATION HERE
val_date = datetime.date(2022, 10, 13)
tenorSOFR = [ "SOFR3M", "SOFR6M", "SOFR12M" ]
rateSOFR = [3.86361,4.23993,4.47309] 
tenorEURIBOR = [ "EURIBOR3M", "EURIBOR6M", "EURIBOR12M" ]
rateEURIBOR = [1.3780,2.0120,2.6610] #in percentage
dailyMaturities = []
monthlyMaturities = [3, 6, 12]
lenOfMaturity = len(monthlyMaturities)
lenOfMaturityPlusValueDate = len(monthlyMaturities) + 1
numberOfDays=0
result=0.0
dayCountBase = 360
SOFR = []
valuationDate = datetime.date(2022, 10, 13)

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


#Calculate the discount rate for rates
def discountRATES_2(rate):
    RATES=[]
    for x in range(len(maturityInDays)):
        numberOfDays = (maturities[x] - val_date).days
        result = 1/(1+ (rate[x]/100.0 * numberOfDays/dayCountBase))
        RATES.append(result)
        result=0.0
    return RATES

#Function to calculate the implied forward rate
def impliedForwardRate(observedRates, RATES):
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
    




#To Display Rates - Original SONIA, Discount Rates and Implied Forward Rates
def ratePrinter_2(rateDF):
    print("")
    print("ORIGINAL RATE, DISCOUNT RATE AND  IMPLIED FORWARD RATE")
    print("__________________________________________________________________")
    print("")
    print(rateDF.to_string())
    

    
    
def createCurrencyLegTable(rate, tenor):
    
    maturities, maturityInDays = getMaturityDates()
    DF, DF["Tenor"],DF["DateRateObserved"] = pd.DataFrame(), tenor,[valuationDate]*3
    #rate = [x+spreadToUse for x in rate]
    DF["observedRates"] = rate
    DF["Maturities"] = maturities
    DF["maturityInDays"] = maturityInDays
    thisRate = discountRATES_2(rate)
    DF["discountRates"] = thisRate
    thisForwardRate = copy.deepcopy(impliedForwardRate(rate,thisRate))
    DF["forwardRates"] = thisForwardRate
    print()
    #ratePrinter_2(DF)
    print()
    DF = pd.merge(paymentDateDF, DF, on="Maturities", how='outer')
    DF = DF.sort_values('Maturities', ascending=True)
    
    DF["DateRateObserved"] = [val_date] * 4
    DF["Type"] = ["Observed", "Observed",  "Interpolated","Observed" ]
    DF["Tenor"] = [ "3M", "6M", "9M","12M" ]
    newPaymentDates = []
    for x in range(len(DF)):
        if x == 0:
            newPaymentDates.append((valuationDate + relativedelta(months=3)-valuationDate).days)
        elif x == 1:
            newPaymentDates.append((valuationDate + relativedelta(months=6)-valuationDate).days)
        elif x == 2:
            newPaymentDates.append((valuationDate + relativedelta(months=9)-valuationDate).days)
        elif x == 3:
            newPaymentDates.append((valuationDate + relativedelta(months=12)-valuationDate).days)
        
    DF["maturityInDays"] = newPaymentDates
    DF = DF.interpolate()
    
    DF = DF[['Maturities',  'Type','Tenor', 'DateRateObserved', 'observedRates', 'maturityInDays', 'discountRates', 'forwardRates']]
    
    DF["Exp"] = [[0,3],[3,6],[6,9],[9,12]]
    return DF




def floatingRateDiscValBaseCurrency(rate, tenor, spreadToUse):
    rate = [x+spreadToUse for x in rate]
    BaseCurrencyDF = createCurrencyLegTable(rate,  tenor)
    impliedForwardRate = BaseCurrencyDF["forwardRates"].tolist()
    discountRate = BaseCurrencyDF["discountRates"].tolist()
    maturityInDays = BaseCurrencyDF["maturityInDays"].tolist()
    res = []
    for x in range(len(maturityInDays)):
        if x == 0:
            temp = maturityInDays[x]/360 * impliedForwardRate[x] * discountRate[x]
            res.append(temp)
        elif x > 0:
            temp = (maturityInDays[x]-maturityInDays[x-1])/360 * impliedForwardRate[x] * discountRate[x]
            res.append(temp)
    return res

def floatingRateDiscValOtherCurrency(rate, tenor, spreadToUse):
    rate = [x+spreadToUse for x in rate]
    OtherCurrencyDF = createCurrencyLegTable(rate,  tenor)
    impliedForwardRate = OtherCurrencyDF["forwardRates"].tolist()
    discountRate = OtherCurrencyDF["discountRates"].tolist()
    maturityInDays = OtherCurrencyDF["maturityInDays"].tolist()
    res = []
    for x in range(len(maturityInDays)):
        if x == 0:
            temp = maturityInDays[x]/360 * impliedForwardRate[x] * discountRate[x]
            res.append(temp)
        elif x > 0:
            temp = (maturityInDays[x]-maturityInDays[x-1])/360 * impliedForwardRate[x] * discountRate[x]
            res.append(temp)
    return res


print(createCurrencyLegTable(rateSOFR, tenorSOFR))
print()
"""
The Spread over SOFR Term Rates if EURIBOR is the Base Currency is: -1.9411784850503233
"""
print(createCurrencyLegTable(rateEURIBOR,  tenorEURIBOR))
print()
"""
The Spread over EURIBOR Term Rates if SOFR is the Base Currency is: 1.9879871667665452
"""


floatingRateDiscValBaseCurrency(rateSOFR, tenorSOFR, 0)
floatingRateDiscValOtherCurrency(rateEURIBOR, tenorEURIBOR, 0)

def calCoupDiscFactors(rateBase, tenorBase, rateOther, tenorOther, exchangeRate):
    def optimizationFunc(r):
        a = floatingRateDiscValOtherCurrency(rateOther, tenorOther, r[0])
        a = sum(a)
        b = floatingRateDiscValBaseCurrency(rateBase, tenorBase, 0.0)
        b = sum(b)*exchangeRate
        
        return b - a
    solutions = fsolve(optimizationFunc, [0.5/100], xtol=1.49012e-08,)
    spreadtoUse = solutions[0]
    return spreadtoUse

print()
spreadPricing = calCoupDiscFactors(rateEURIBOR,tenorEURIBOR, rateSOFR, tenorSOFR, 0.97782)
print(f"The Spread over SOFR Term Rates if EURIBOR is the Base Currency is: {spreadPricing}")   
"""
2.49984316448582
"""    

print()
spreadPricing = calCoupDiscFactors( rateSOFR, tenorSOFR,rateEURIBOR,tenorEURIBOR, 1/0.97782)
print(f"The Spread over EURIBOR Term Rates if SOFR is the Base Currency is: {spreadPricing}")       
"""
2.499843164485829
"""


"""
Validation Process: If we set EURO as the base currency and SOFR as the other
currency. Then we can verify our calculations like below:
"""
rateSOFR_2 = [x+(-1.9411784850503233) for x in rateSOFR]

print(sum(floatingRateDiscValOtherCurrency(rateSOFR_2, tenorSOFR, 0)))
"""
2.49984316448582
"""

print(sum(floatingRateDiscValBaseCurrency(rateEURIBOR, tenorEURIBOR, 0))*0.97782)
"""
2.49984316448582
"""


"""
Validation Process: If we set SOFR as the base currency and EURO as the other
currency. Then we can verify our calculations like below:
"""
rateEURIBOR_2 = [x+(1.9879871667665452) for x in rateEURIBOR]

print(sum(floatingRateDiscValOtherCurrency(rateEURIBOR_2, tenorEURIBOR, 0))*(0.97782))
"""
4.348214655086883
"""

print(sum(floatingRateDiscValBaseCurrency(rateSOFR, tenorSOFR, 0)))
"""
4.348214655086925
"""
