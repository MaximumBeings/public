#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 16:20:07 2022

@author: oluwaseyiawoga
"""

import datetime
import pandas as pd
from dateutil.relativedelta import relativedelta
from datetime import date, timedelta
import locale
import math
import copy
locale.setlocale(locale.LC_ALL, '')
pd.set_option('display.precision',10)



"""
Topic: Multi Instrument Swap Curve Construction
Source: Ron Uri - A Practical Guide to Swap Curve Contruction - Bank of Canada (Google it).
Discussion:  To develop a multi-instrument swap curve construction program in python per the above article.  Excluding
the effect of convexity adjustment which will be addressed at a later time.  Program is a prototype and not working
properly.  We will revisit shortly and rewrite the program from the top.  Posted as a work-in-progress.  It will be a great 
addition to our yield curve library when fully done. See you next time.

A Practical Guide to Swap Curve Construction, Bank of Canada, 30 Years SOFR Swap Zero Rates & Discount Curves & Python.

This post moves us closer to production level implementation of our fixed income recipes. This one is implements an article by the Bank of Canada on swap curve construction. Specifically, the recommends constructing the swap curve for long dated (like 30 years) as follows:

SHORT-END OF THE CURVE: 

The short end of the swap curve, out to three months, is based on the overnight, one-month, two-month and three-month deposit rates. The short-end deposit rates are inherently zero-coupon rates and need only be  converted to the base currency swap rate compounding frequency and day count convention. T

THE MIDDLE AREA OF THE SWAP CURVE:

The middle area of the swap curve up to two years is derived from either FRA rates or interest rate futures contracts.  FRAs are preferable , as they carry a fixed time horizon to settlement and settle at maturity , whereas futures contracts have a fixed settlement date and are marked to market daily.  FRAs for most currencies, however, are not observable or  suffer from lack of liquidity. On the other hand, futures contracts are exchange traded, rendering them more uniform, liquid and transparent.  Extracting forward rates from futures rates requires a convexity adjustment.
It is an adjustment for the difference in convexity characteristics of futures contracts and forward rates.

We assumed that your data vendor e.g. Bloomberg or Refinitiv supply you with the convexity adjustment. But in the near future we will develop our own model to calculate convexity adjustment.  

THE LONG END OF THE CURVE:
The long end of the swap curve out to ten years is derived directly from observable coupon swap rates. These are generic plain vanilla interest rate swaps with exchanged rates exchanged for floating interest rates. In this implementation, we used the SOFR SWAP rates obtained from the CME website.

This articles uses continuously compounding to do the calculations but in a future post, we will discount how to accomplish the same objective using discrete time compounding. The code can be obtained from the author’s GitHub page at the link below:



Sources:
(1) https://www.bankofcanada.ca/2000/08/working-paper-2000-17/
(2) https://www.cmegroup.com/trading/interest-rates/cleared-otc-sofr-swaps.html

"""



"""
USD SOFR - Overnight        3.0500%
USD SOFR Term - 1 Month     3.78625%
USD SOFR Term - 3 Months    4.14091%
"""



val_date = datetime.date(2022, 11, 1)
rate = [3.0500/100.0,3.78625/100.0,4.14091/100.0]
rateMaturities = [val_date + timedelta(days=1),val_date + relativedelta(months=1),val_date+relativedelta(months=3)]

def rateMatInDaysFunctn(val_date, rateMaturities):
    rateMatInDays = []
    for x in range(len(rateMaturities)):
        rateMatInDays.append((rateMaturities[x] - val_date).days)
    return rateMatInDays

rateMatInDays_N = rateMatInDaysFunctn(val_date, rateMaturities)



"""
THE SHORT-END OF THE SWAP CURVE:
    
The short end of the swap curve, out to three months, is based on the
overnight, one-month, two-month and three-month deposit rates. The short-end
deposit rates are inherently zero-coupon rates and need only be 
converted to the base currency swap rate compounding frequency and day count
convention. The following equation is used to compute the continously compounded
zero swap rate for deposit rates:
    
    rc = ty/tm * ln(1 + rd/(ty/tm))
    where
    rd = observed deposit rate
    tm = represents the number of days to maturity
    ty = represents number of days in a year as specified according
    to the day count convention used.
"""


ty = 360  #day count convention  -- represents number of days in a year as specified according
def zeroRateDeposits(ty, rate, rateMatInDays):
    rc = []
    for x in range(len(rateMatInDays)):
        rc.append((ty/rateMatInDays[x]) * math.log(1 + rate[x]/(ty/rateMatInDays[x])))
    return rc


time = copy.deepcopy(rateMatInDaysFunctn(val_date, rateMaturities))
zeroRatesD = copy.deepcopy(zeroRateDeposits(ty, rate, rateMatInDays_N))


def disc_factor():
    #Using the zero rates calculated above we calculate our discount factors as documented below.
    #This program returns a vector of discount factors for the different cashflow payments
    disc_factor = []
    for x in range(len(time)):
        disc_factor.append(math.exp(-1* time[x]/360.0*zeroRatesD[x]))
    return disc_factor
    
zeroDiscounts = disc_factor()



d = {'Maturities' : pd.Series(rateMaturities),'Number_of_Days' : pd.Series(time),'LIBOR_Rates' : pd.Series(rate),'Zero_Rates' : pd.Series(zeroRatesD),'Discount_Rates' : pd.Series(zeroDiscounts)}

df = pd.DataFrame(d,columns=['Maturities', 'Number_of_Days', 'LIBOR_Rates','Zero_Rates', 'Discount_Rates'])

print()
print(df.to_string(index=False))

"""
The output so far look like so:
    
Maturities  Number_of_Days  LIBOR_Rates    Zero_Rates  Discount_Rates
2022-11-02               1    0.0305000  0.0304987081    0.9999152850
2022-12-01              30    0.0378625  0.0378028933    0.9968547157
2023-02-01              92    0.0414091  0.0411915313    0.9895284874

"""

"""
THE MIDDLE AREA OF THE SWAP CURVE:
    
Futures Prices  (Assumed)
May 1st, 2023             95.08485
Nov 1st, 2023             95.13059
Feb 1st, 2024             95.28610           
May 1st, 2024             95.38650
Aug 1st, 2024             95.58650


The middle area of the swap curve up to two years is derived from
either FRA rates or interest rate futures contracts.  FRAs are preferable
, as they carry a fixed time horizon to settlement and settle at maturity
, whereas futures contracts have a fixed settlement date and are marked
to market daily.  FRAs for most currencies, however, are not observable or 
suffer from lack of liquidity. On the other hand, futures contracts are
exchange traded, rendering them more uniform, liquid and transparent. 

Extracting forward rates from futures rates requires a convexity adjustment.
It is an adjustment for the difference in convexity characteristics of futures
contracts and forward rates.

We will assume that your data vendor e.g. Bloomberg supply you with
the convexity adjustment. But in the near future we will develop our own model
to calculate convexity adjustment.  In order to calculate convexity adjustment, we
need to cover the vasicek model and GARCH first.  So next time we cover vasicek model
and then GARCH and develop the convexity adjustment model and update this program.
***In this program we assume therefore that convexity adjustment is zero
futures prices = 100 - future interest rate * 100
"""

futurePrices = [95.08485, 95.13059, 95.28610 ,95.38650, 95.58650]
#The first step is to convert the futures prices into future interest rate using the above formula


def futureInterestRate(futurePrices):
    fInterestRate = []
    for x in range(len(futurePrices)):
        fInterestRate.append((futurePrices[x] - 100.0)/(-1*100.0))
    return fInterestRate
    
ratesF = copy.deepcopy(futureInterestRate(futurePrices))
    
rateMaturitiesFutures = [datetime.date(2023, 5, 1),datetime.date(2023, 11, 1),datetime.date(2024, 2, 1),datetime.date(2024, 5, 1), \
                        datetime.date(2024, 8, 1)]
                 
lastDepositDate = datetime.date(2023, 2, 1)  



def rateDaysFurtures(val_date, rateMaturitiesFutures):
    rateMatInDaysFutures = []
    for x in range(len(rateMaturitiesFutures)):
        rateMatInDaysFutures.append((rateMaturitiesFutures[x] - val_date).days)
        
    return rateMatInDaysFutures

numOfDaysF = copy.deepcopy(rateDaysFurtures(val_date, rateMaturitiesFutures))

ty = float(360)  #day count convention

lastDepositDate2 = (datetime.date(2023, 2, 1) - val_date).days

def contCompFuturesRate(ty, ratesF, numOfDaysF):
    rc = []
    
    for x in range(len(numOfDaysF)):
        if x == 0:
            rc.append((ty/(numOfDaysF[x]-lastDepositDate2)) * math.log(1 + ratesF[x]/(ty/(numOfDaysF[x]-lastDepositDate2))))
        elif x > 0:
            rc.append((ty/(numOfDaysF[x]-numOfDaysF[x-1])) * math.log(1 + ratesF[x]/(ty/(numOfDaysF[x]-numOfDaysF[x-1]))))
    return rc

"""
The continuously compounded future rate is then converted to a 
continously compounded zero rate using the following transformation:
    
    r2 =( rf * (t2 - t1) + r1 * t1) / t2
    
    where 
    rf = is the continusously compounded future rate for the period
    between t1 and t2 and r2 are the continuously compounded zero
    rates for maturities t1 and t2 respectively.
"""

ContFuture = copy.deepcopy(contCompFuturesRate(ty, ratesF, numOfDaysF))

##Get the zero rates from continously compounded futures interest rates

def zeroRateFutures(numOfDaysF, ContFuture,time,zeroRatesD):
    #zeroRF = []
    r2 = []
    for x in range(len(numOfDaysF)):
        if x == 0:
            r2.append((ContFuture[x] * (numOfDaysF[x] - time[-1]) + (zeroRatesD[-1]*time[-1]))/numOfDaysF[x])
        elif x > 0:
            r2.append((ContFuture[x] * (numOfDaysF[x] - numOfDaysF[x-1]) + (r2[x-1]*numOfDaysF[x-1]))/numOfDaysF[x])
    return r2
            
zeroRatesF = copy.deepcopy(zeroRateFutures(numOfDaysF, ContFuture,time,zeroRatesD))

#Discount Factors for Futures Rate
def disc_factor_2():
    #Using the zero rates calculated above we calculate our discount factors as documented below.
    #This program returns a vector of discount factors for the different cashflow payments
    disc_factor = []
    for x in range(len(numOfDaysF)):
        disc_factor.append(math.exp(-1* numOfDaysF[x]/360.0*zeroRatesF[x]))
    return disc_factor

discFactorsFutures = disc_factor_2()
    
midlevelMaturities = rateMaturities + rateMaturitiesFutures
Number_of_DaysMidlevel = time + numOfDaysF
Orignal_Rates = rate + ratesF
Orignal_Rates2 = [x * 100 for x in Orignal_Rates]
zeroRatesMidlevel = zeroRatesD + zeroRatesF
discountFactorsMidlevel =  zeroDiscounts + discFactorsFutures
Instrument = ["Deposit", "Deposit", "Deposit","Futures", "Futures","Futures","Futures","Futures"]


dMidLevel = {'Maturities' : pd.Series(midlevelMaturities),'Number_of_Days' : pd.Series(Number_of_DaysMidlevel),'Instrument' : pd.Series(Instrument),'Original_Rates_(%)' : pd.Series(Orignal_Rates2),'Zero_Rates' : pd.Series(zeroRatesMidlevel),'Discount_Rates' : pd.Series(discountFactorsMidlevel)}

df = pd.DataFrame(dMidLevel,columns=['Maturities', 'Number_of_Days', 'Instrument','Original_Rates_(%)','Zero_Rates', 'Discount_Rates'])

print
print(df.to_string(index=False))




"""
MID-LEVEL RATES:
    
Maturities  Number_of_Days Instrument  Original_Rates_(%)    Zero_Rates  Discount_Rates
 2022-11-02               1    Deposit             3.05000  0.0304987081    0.9999152850
 2022-12-01              30    Deposit             3.78625  0.0378028933    0.9968547157
 2023-02-01              92    Deposit             4.14091  0.0411915313    0.9895284874
 2023-05-01             181    Futures             4.91515  0.0449598885    0.9776487421
 2023-11-01             365    Futures             4.86941  0.0465418498    0.9539077938
 2024-02-01             457    Futures             4.71390  0.0466053594    0.9425532010
 2024-05-01             547    Futures             4.61350  0.0464845281    0.9318059837
 2024-08-01             639    Futures             4.41350  0.0461106869    0.9214134131

"""







"""
REPRESENTATION OF OBSERVED RATES:
    
Maturities        Observed Rate       
2024-11-01        4.6146 
2025-11-01        4.3415
2027-11-01        4.0448
2032-11-01        3.8316
2042-11-01        3.6943
2052-11-01        3.4076
         
         

"""
observedRatesM = [datetime.date(2024, 11, 1),datetime.date(2025, 11, 1),datetime.date(2027,11,1),datetime.date(2032, 11, 1), \
                        datetime.date(2042, 11, 1),datetime.date(2052, 11, 1)]
                        
                        
observedRate = [4.6146, 4.3415, 4.0448, 3.8316, 3.6943,3.4076 ]

RatesObserved = {'Maturities' : pd.Series(observedRatesM),'Observed_Rates' : pd.Series(observedRate)}

Observed = pd.DataFrame(RatesObserved,columns=['Maturities', 'Observed_Rates'])

print
print(Observed.to_string(index=False))





RequiedDates = [datetime.date(2024,11,1), datetime.date(2025,2,1), datetime.date(2025,5,1), datetime.date(2025,8,1), \
                datetime.date(2025,11,1), datetime.date(2026,2,1), datetime.date(2026,5,1), datetime.date(2026,8,1), \
                datetime.date(2026,11,1), datetime.date(2027,2,1), datetime.date(2027,5,1), datetime.date(2027,8,1), \
                datetime.date(2027,11,1), datetime.date(2028,2,1), datetime.date(2028,5,1), datetime.date(2028,8,1), \
                datetime.date(2028,11,1), datetime.date(2029,2,1), datetime.date(2029,5,1), datetime.date(2029,8,1), \
                datetime.date(2029,11,1), datetime.date(2030,2,1), datetime.date(2030,5,1), datetime.date(2030,8,1),\
                datetime.date(2030,11,1), datetime.date(2031,2,1), datetime.date(2031,5,1), datetime.date(2031,8,1),\
                datetime.date(2031,11,1), datetime.date(2032,2,1), datetime.date(2032,5,1), datetime.date(2032,8,1),\
                datetime.date(2032,11,1), datetime.date(2033,2,1), datetime.date(2033,5,1), datetime.date(2033,8,1),\
                datetime.date(2033,11,1), datetime.date(2034,2,1), datetime.date(2034,5,1), datetime.date(2034,8,1),\
                datetime.date(2034,11,1), datetime.date(2035,2,1), datetime.date(2035,5,1), datetime.date(2035,8,1),\
                datetime.date(2035,11,1), datetime.date(2036,2,1), datetime.date(2036,5,1), datetime.date(2036,8,1),\
                datetime.date(2036,11,1), datetime.date(2037,2,1), datetime.date(2037,5,1), datetime.date(2037,8,1),\
                datetime.date(2037,11,1), datetime.date(2038,2,1), datetime.date(2038,5,1), datetime.date(2038,8,1),\
                datetime.date(2038,11,1), datetime.date(2039,2,1), datetime.date(2039,5,1), datetime.date(2039,8,1),\
                datetime.date(2039,11,1), datetime.date(2040,2,1), datetime.date(2040,5,1), datetime.date(2040,8,1),\
                datetime.date(2040,11,1), datetime.date(2041,2,1), datetime.date(2041,5,1), datetime.date(2041,8,1),\
                datetime.date(2041,11,1), datetime.date(2042,2,1), datetime.date(2042,5,1), datetime.date(2042,8,1),\
                datetime.date(2042,11,1), datetime.date(2043,2,1), datetime.date(2043,5,1), datetime.date(2043,8,1),\
                datetime.date(2043,11,1), datetime.date(2044,2,1), datetime.date(2044,5,1), datetime.date(2044,8,1),\
                datetime.date(2044,11,1), datetime.date(2045,2,1), datetime.date(2045,5,1), datetime.date(2045,8,1),\
                datetime.date(2045,11,1), datetime.date(2046,2,1), datetime.date(2046,5,1), datetime.date(2046,8,1),\
                datetime.date(2046,11,1), datetime.date(2047,2,1), datetime.date(2047,5,1), datetime.date(2047,8,1),\
                datetime.date(2047,11,1),datetime.date(2048,2,1),datetime.date(2048,5,1),datetime.date(2048,8,1),\
                datetime.date(2048,11,1),datetime.date(2049,5,1),datetime.date(2049,8,1),datetime.date(2049,11,1),\
                datetime.date(2050,2,1),datetime.date(2050,5,1),datetime.date(2050,8,1),datetime.date(2050,11,1),\
                datetime.date(2051,2,1),datetime.date(2051,5,1),datetime.date(2051,8,1),datetime.date(2051,11,1),\
                datetime.date(2052,2,1),datetime.date(2052,5,1),datetime.date(2052,8,1),datetime.date(2052,11,1)
]
                        
RequiredDatesM = {'Maturities' : pd.Series(RequiedDates)}
RequiredDatesMN = pd.DataFrame(RequiredDatesM,columns=['Maturities'])
print
print(RequiredDatesMN.to_string(index=False))



CombDF = pd.merge(RequiredDatesMN, Observed, on='Maturities', how='outer')

InterpolatedRatesDF = CombDF.interpolate(method='linear')  #Interpolate Using Linear Methodology.

print
print(CombDF.to_string(index=False))



print
print(InterpolatedRatesDF.to_string(index=False))







interPolatedSFRDates = InterpolatedRatesDF['Maturities'].values.tolist()
interPolatedSFRRates = InterpolatedRatesDF['Observed_Rates'].values.tolist()
SFRStartingDate = datetime.date(2024, 11, 1)
SFRStartingIndex = interPolatedSFRDates.index(SFRStartingDate)
SFRDatesToBeBootStrapped = interPolatedSFRDates[SFRStartingIndex:]
SFRToBeBootStrapped = interPolatedSFRRates[SFRStartingIndex:]

#df
#The first 3 month from valuation date states from index 4
midLevelZeroRatesDates = df['Maturities'].values.tolist()[4:]
midLevelZeroRates = df['Zero_Rates'].values.tolist()[4:]




def discountSFRhelper(midLevelZeroRatesDates,midLevelZeroRates,SFRToBeBootStrapped):
    final = 0.0
    ans = 0.0
    for x in range(len(midLevelZeroRatesDates)):
        numberOfDays = (midLevelZeroRatesDates[x] - val_date).days
        ans = (SFRToBeBootStrapped)/4.0 * math.exp(-1*midLevelZeroRates[x]*numberOfDays/360.0)
        final = final + ans
    return final
    



def swapRateCalculator(midLevelZeroRatesDates,midLevelZeroRates,SFRToBeBootStrapped,SFRDatesToBeBootStrapped):
    ans = 0.0
    ansB= 0.0
    ansC = 0.0
    ansD = 0.0
    for x in range(len(SFRToBeBootStrapped)):
        ansA = 100 -  discountSFRhelper(midLevelZeroRatesDates,midLevelZeroRates,SFRToBeBootStrapped[x])
        ansB = 100+(SFRToBeBootStrapped[x])/4.0
        ansC = -1 * math.log(ansA/ansB)
        ansD = ((SFRDatesToBeBootStrapped[x] - val_date).days)/360.0
        ans = ansC / ansD
        midLevelZeroRates.append(ans)
        midLevelZeroRatesDates.append(SFRDatesToBeBootStrapped[x])
    return midLevelZeroRates

longy=[]
longy = swapRateCalculator(midLevelZeroRatesDates,midLevelZeroRates,SFRToBeBootStrapped,SFRDatesToBeBootStrapped)
longy2 = longy[4:]

#Discount Factors for Futures Rate
def disc_factor_3():
    #Using the zero rates calculated above we calculate our discount factors as documented below.
    #This program returns a vector of discount factors for the different cashflow payments
    disc_factor = []
    for x in range(len(SFRDatesToBeBootStrapped)):
        numOfDaysF = (SFRDatesToBeBootStrapped[x] - val_date).days
        disc_factor.append(math.exp(-1* numOfDaysF/360.0*longy2[x]))
    return disc_factor
    
Swap_Discount = disc_factor_3()
    
    
RatesObserved = {'Swap_Maturities' : pd.Series(SFRDatesToBeBootStrapped),'Swap_Observed_Rates' : pd.Series(SFRToBeBootStrapped),'Swap_Zero_Rates' : pd.Series(longy2),'Swap_Discount_Rates' : pd.Series(Swap_Discount)}

Swwwap = pd.DataFrame(RatesObserved,columns=['Swap_Maturities', 'Swap_Observed_Rates','Swap_Zero_Rates','Swap_Discount_Rates'])

print
print(Swwwap.to_string(index=False))


midlevelMaturities = rateMaturities + rateMaturitiesFutures
Number_of_DaysMidlevel = time + numOfDaysF
Orignal_Rates = rate + ratesF
Orignal_Rates2 = [x * 100 for x in Orignal_Rates]
zeroRatesMidlevel = zeroRatesD + zeroRatesF
discountFactorsMidlevel =  zeroDiscounts + discFactorsFutures

Maturities = midlevelMaturities + SFRDatesToBeBootStrapped
finalRates = Orignal_Rates + SFRToBeBootStrapped
finalZeroRates = zeroRatesMidlevel + longy2
finalDiscount = discountFactorsMidlevel + Swap_Discount

RatesObserved = {'Maturities' : pd.Series(Maturities),'Rates' : pd.Series(finalRates),'Zero_Rates' : pd.Series(finalZeroRates),'Discount_Rates' : pd.Series(finalDiscount)}
final = pd.DataFrame(RatesObserved,columns=['Maturities', 'Rates','Zero_Rates','Discount_Rates'])

print
print(final.to_string(index=False))


numberOfDays = (datetime.date(2052,11,1) - datetime.date(2024,11,1)).days
elongatedMaturities = []
for x in range(1,numberOfDays+2):
    elongatedMaturities.append(val_date + timedelta(days=x))



Final3 = {'Maturities' : pd.Series(elongatedMaturities)}
Final4 = pd.DataFrame(Final3,columns=['Maturities'])
print
print(Final4.to_string(index=False))

CombDF = pd.merge(Final4, final, on='Maturities', how='outer')

InterpolatedRatesDF = CombDF.interpolate(method='linear')  #Interpolate Using Linear Methodology.

print
print(InterpolatedRatesDF.to_string(index=False))

