#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 20:48:31 2020

@author: oluwaseyiawoga
"""
"""
Slightly refactored from an old code for a paper entitled - LIBOR Transitions - Matters Arising.
"""

"""
Import relevant packages and libraries
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
Read the data for the short-end of the yield curve
into the program/model
"""

"""
USD LIBOR - Overnight       0.36740%
USD LIBOR - 1 Week          0.39000%
USD LIBOR - 1 Month         0.41750%
USD LIBOR - 2 Months        0.50970%
USD LIBOR - 3 Months        0.59435%
"""

val_date = datetime.date(2015, 12, 23)
rate = [0.36740/100.0,0.390000/100.0,0.41750/100.0,0.50970/100.0,0.59435/100.0]
rateMaturities = [val_date + timedelta(days=1),val_date + timedelta(weeks=1),val_date \
+ relativedelta(months=1),val_date+relativedelta(months=2),val_date+relativedelta(months=3)]

def rateMatInDaysFunctn(val_date, rateMaturities):
    rateMatInDays = []
    for x in range(len(rateMaturities)):
        rateMatInDays.append((rateMaturities[x] - val_date).days)
    return rateMatInDays

rateMatInDays_N = rateMatInDaysFunctn(val_date, rateMaturities)


"""
THE SHORT-END OF THE SWAP CURVE - FORMULA:
    
The short end of the swap curve, out to three months, is based on the overnight, 
one-month, two-month and three-month deposit rates. The short-end deposit rates 
are inherently zero-coupon rates and need only be converted to the base currency 
swap rate compounding frequency and day count convention. The following equation 
is used to compute the continously compounded zero swap rate for deposit rates:
    
    rc = ty/tm * ln(1 + rd/(ty/tm))
    where
    rd = observed deposit rate
    tm = represents the number of days to maturity
    ty = represents number of days in a year as specified according
    to the day count convention used.
"""

ty = 360  #day count convention  


def zeroRateDeposits(ty, rate, rateMatInDays):
    rc = []
    for x in range(len(rateMatInDays)):
        rc.append((ty/rateMatInDays[x]) * math.log(1 + rate[x]/(ty/rateMatInDays[x])))
    return rc


time = copy.deepcopy(rateMatInDaysFunctn(val_date, rateMaturities))
zeroRatesD = copy.deepcopy(zeroRateDeposits(ty, rate, rateMatInDays_N))


def disc_factor():
    #Using the zero rates calculated above we calculate our 
    #discount factors as documented below. This program returns 
    #a vector of discount factors for the different cashflow payments.
    
    disc_factor = []
    for x in range(len(time)):
        disc_factor.append(math.exp(-1* time[x]/360.0*zeroRatesD[x]))
    return disc_factor
    
zeroDiscounts = disc_factor()



d = {'Maturities' : pd.Series(rateMaturities),'LIBOR_Rates' : pd.Series(rate),'Zero_Rates' \
: pd.Series(zeroRatesD),'Discount_Rates' : pd.Series(zeroDiscounts)}

df = pd.DataFrame(d,columns=['Maturities', 'LIBOR_Rates','Zero_Rates', 'Discount_Rates'])

print
print(df.to_string(index=False))

"""
Preview the Zero Rate for the Short-End:
    
 Maturities  LIBOR_Rates   Zero_Rates  Discount_Rates
 2015-12-24    0.0036740  0.003673981     0.999989795
 2015-12-30    0.0039000  0.003899851     0.999924172
 2016-01-23    0.0041750  0.004174208     0.999640619
 2016-02-23    0.0050970  0.005094404     0.999123015
 2016-03-23    0.0059435  0.005937620     0.998500227


"""



"""
THE MIDDLE AREA OF THE SWAP CURVE:
    
Futures Prices for June 30, Sept 30 and Dec 31, 2014 (Assumed)
June 30th, 2016             99.115
Sept 30th, 2016             98.960
Dec  31st, 2016             98.800
Mar 31st, 2017              98.655
June 30th, 2017             98.515
Sept 30th, 2017             98.390
Dec 31st, 2017              98.275

The middle area of the swap curve up to two years is derived from either 
FRA rates or interest rate futures contracts.  FRAs are preferable, as 
they carry a fixed time horizon to settlement and settle at maturity, 
whereas futures contracts have a fixed settlement date and are marked
to market daily.  FRAs for most currencies, however, are not observable 
or suffer from lack of liquidity. On the other hand, futures contracts 
are exchange traded, rendering them more uniform, liquid and transparent. 

Extracting forward rates from futures rates requires a convexity adjustment.
It is an adjustment for the difference in convexity characteristics of futures
contracts and forward rates.

We will assume that your data vendor e.g. Bloomberg supply you with the convexity 
adjustment. In this program we assume therefore that convexity adjustment is zero
futures prices = 100 - future interest rate * 100
"""

futurePrices = [99.115,98.960,98.800,98.655,98.515,98.390,98.275]

#The first step is to convert the futures prices 
#into future interest rate using the above formula


def futureInterestRate(futurePrices):
    fInterestRate = []
    for x in range(len(futurePrices)):
        fInterestRate.append((futurePrices[x] - 100.0)/(-1*100.0))
    return fInterestRate
    
ratesF = copy.deepcopy(futureInterestRate(futurePrices))
    
rateMaturitiesFutures = [datetime.date(2016, 6, 30),datetime.date(2016, 9, 30),\
                        datetime.date(2016, 12, 31),datetime.date(2017, 3, 31), \
                        datetime.date(2017, 6, 30),datetime.date(2017, 9, 30),\
                        datetime.date(2017, 12, 31)]
                 
lastDepositDate = datetime.date(2016, 3, 23)  



def rateDaysFurtures(val_date, rateMaturitiesFutures):
    rateMatInDaysFutures = []
    for x in range(len(rateMaturitiesFutures)):
        rateMatInDaysFutures.append((rateMaturitiesFutures[x] - val_date).days)
        
    return rateMatInDaysFutures

numOfDaysF = copy.deepcopy(rateDaysFurtures(val_date, rateMaturitiesFutures))

ty = float(360)  #day count convention

lastDepositDate2 = (datetime.date(2016, 3, 23) - val_date).days

def contCompFuturesRate(ty, ratesF, numOfDaysF):
    rc = []
    
    for x in range(len(numOfDaysF)):
        if x == 0:
            rc.append((ty/(numOfDaysF[x]-lastDepositDate2)) * \
            math.log(1 + ratesF[x]/(ty/(numOfDaysF[x]-lastDepositDate2))))
        elif x > 0:
            rc.append((ty/(numOfDaysF[x]-numOfDaysF[x-1])) * \
            math.log(1 + ratesF[x]/(ty/(numOfDaysF[x]-numOfDaysF[x-1]))))
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
            r2.append((ContFuture[x] * (numOfDaysF[x] - time[-1]) \
            + (zeroRatesD[-1]*time[-1]))/numOfDaysF[x])
        elif x > 0:
            r2.append((ContFuture[x] * (numOfDaysF[x] - numOfDaysF[x-1])\
            + (r2[x-1]*numOfDaysF[x-1]))/numOfDaysF[x])
    return r2
            
zeroRatesF = copy.deepcopy(zeroRateFutures(numOfDaysF, ContFuture,time,zeroRatesD))
#Discount Factors for Futures Rate

def disc_factor_2():
    #Using the zero rates calculated above we calculate our discount factors 
    #as documented below. This program returns a vector of discount factors 
    #for the different cashflow payments
    disc_factor = []
    for x in range(len(numOfDaysF)):
        disc_factor.append(math.exp(-1* numOfDaysF[x]/360.0*zeroRatesF[x]))
    return disc_factor

discFactorsFutures = disc_factor_2()
    
midlevelMaturities = rateMaturities + rateMaturitiesFutures
Number_of_DaysMidlevel = time + numOfDaysF
Orignal_Rates = rate + ratesF
#Orignal_Rates2 = [x * 100.0 for x in Orignal_Rates]
zeroRatesMidlevel = zeroRatesD + zeroRatesF
discountFactorsMidlevel =  zeroDiscounts + discFactorsFutures


dMidLevel = {'Maturities' : pd.Series(midlevelMaturities),'Original_Rates_(%)' : \
pd.Series(Orignal_Rates),'Zero_Rates' : pd.Series(zeroRatesMidlevel),\
'Discount_Rates' : pd.Series(discountFactorsMidlevel)}

df = pd.DataFrame(dMidLevel,columns=['Maturities', \
'Original_Rates_(%)','Zero_Rates', 'Discount_Rates'])

print
print(df.to_string(index=False))

"""
MID-LEVEL RATES:
    
Maturities  Original_Rates_(%)   Zero_Rates  Discount_Rates
 2015-12-24           0.0036740  0.003673981     0.999989795
 2015-12-30           0.0039000  0.003899851     0.999924172
 2016-01-23           0.0041750  0.004174208     0.999640619
 2016-02-23           0.0050970  0.005094404     0.999123015
 2016-03-23           0.0059435  0.005937620     0.998500227
 2016-06-30           0.0088500  0.007449521     0.996076027
 2016-09-30           0.0104000  0.008407588     0.993435696
 2016-12-31           0.0120000  0.009286766     0.990398474
 2017-03-31           0.0134500  0.010089913     0.987079419
 2017-06-30           0.0148500  0.010865838     0.983388027
 2017-09-30           0.0161000  0.011605411     0.979358510
 2017-12-31           0.0172500  0.012303401     0.975060120

"""

"""
CONSTRUCT LONG-END OF THE YIELD CURVE
"""
#Import observed rates and their maturities
observedRatesM = [datetime.date(2015, 12, 24),datetime.date(2015, 12, 30),datetime.date(2016, 1, 23),\
                        datetime.date(2016, 2, 23), datetime.date(2016, 3, 23),datetime.date(2016, 6, 23),\
                        datetime.date(2016, 9, 23),datetime.date(2016, 12, 23),datetime.date(2017, 3, 23),\
                        datetime.date(2017, 6, 23),datetime.date(2017, 9, 23),datetime.date(2017, 12, 23), \
                        datetime.date(2018, 12, 23),datetime.date(2019, 12, 23),datetime.date(2020, 12, 23),\
                        datetime.date(2021, 12, 23),datetime.date(2022, 12, 23),datetime.date(2023, 12, 23),\
                        datetime.date(2024, 12, 23), datetime.date(2025, 12, 23),datetime.date(2030, 12, 23),\
                        datetime.date(2035, 12, 23),datetime.date(2045, 12, 23)]
                        
                        
observedRate = [0.36740,0.39000,0.41750, 0.50970,0.59435,0.88500,1.04000,1.20000,1.34500,1.48500,1.61000,\
1.72500,1.36600,1.54800,1.69800,1.82600,1.93400,2.02400,2.10200,2.17200,2.40700,2.52000, 2.60800]

RatesObserved = {'Maturities' : pd.Series(observedRatesM),'Observed_Rates' : pd.Series(observedRate)}

Observed = pd.DataFrame(RatesObserved,columns=['Maturities', 'Observed_Rates'])

print
print(Observed.to_string(index=False))

#The dates that maps the underlying tenor
#This should be at least every three months
#in our case. This can be implemented in a 
#function
RequiedDates = [datetime.date(2015, 12, 24),datetime.date(2015, 12, 30),\
               datetime.date(2016, 1, 23),datetime.date(2016, 2, 23), \
               datetime.date(2016, 3, 23),datetime.date(2016, 6, 23),\
               datetime.date(2016, 9, 23),datetime.date(2016, 12, 23),\
               datetime.date(2017, 3, 23),datetime.date(2017, 6, 23),\
               datetime.date(2017, 9, 23),datetime.date(2017, 12, 23), \
               datetime.date(2018, 3, 23),datetime.date(2018, 6, 23),\
               datetime.date(2018, 9, 23),datetime.date(2018, 12, 23),\
               datetime.date(2019, 3, 23),datetime.date(2019, 6, 23),\
               datetime.date(2019, 9, 23),datetime.date(2019, 12, 23), \
               datetime.date(2020, 3, 23),datetime.date(2020, 6, 23),\
               datetime.date(2020, 9, 23),datetime.date(2020, 12, 23), \
               datetime.date(2021, 3, 23),datetime.date(2021, 6, 23),\
               datetime.date(2021, 9, 23),datetime.date(2021, 12, 23),\
               datetime.date(2022, 3, 23),datetime.date(2022, 6, 23),\
               datetime.date(2022, 9, 23),datetime.date(2022, 12, 23), \
               datetime.date(2023, 3, 23),datetime.date(2023, 6, 23),\
               datetime.date(2023, 9, 23),datetime.date(2023, 12, 23), \
               datetime.date(2024, 3, 23),datetime.date(2024, 6, 23),\
               datetime.date(2024, 9, 23),datetime.date(2024, 12, 23), \
               datetime.date(2025, 3, 23),datetime.date(2025, 6, 23),\
               datetime.date(2025, 9, 23),datetime.date(2025, 12, 23), \
               datetime.date(2026, 3, 23),datetime.date(2026, 6, 23),\
               datetime.date(2026, 9, 23),datetime.date(2026, 12, 23), \
               datetime.date(2027, 3, 23),datetime.date(2027, 6, 23),\
               datetime.date(2027, 9, 23),datetime.date(2027, 12, 23), \
               datetime.date(2028, 3, 23),datetime.date(2028, 6, 23),
               datetime.date(2028, 9, 23),datetime.date(2028, 12, 23), \
               datetime.date(2029, 3, 23),datetime.date(2029, 6, 23),\
               datetime.date(2029, 9, 23),datetime.date(2029, 12, 23), \
               datetime.date(2030, 3, 23),datetime.date(2030, 6, 23),\
               datetime.date(2030, 9, 23),datetime.date(2030, 12, 23),\
               datetime.date(2031, 3, 23),datetime.date(2031, 6, 23),\
               datetime.date(2031, 9, 23),datetime.date(2031, 12, 23),\
               datetime.date(2032, 3, 23),datetime.date(2032, 6, 23),\
               datetime.date(2032, 9, 23),datetime.date(2032, 12, 23), \
               datetime.date(2033, 3, 23),datetime.date(2033, 6, 23),\
               datetime.date(2033, 9, 23),datetime.date(2033, 12, 23),\
               datetime.date(2034, 3, 23),datetime.date(2034, 6, 23),\
               datetime.date(2034, 9, 23),datetime.date(2034, 12, 23),\
               datetime.date(2035, 3, 23),datetime.date(2035, 6, 23),\
               datetime.date(2035, 9, 23),datetime.date(2035, 12, 23), \
               datetime.date(2036, 3, 23),datetime.date(2036, 6, 23),\
               datetime.date(2036, 9, 23),datetime.date(2036, 12, 23),\
               datetime.date(2037, 3, 23),datetime.date(2037, 6, 23),\
               datetime.date(2037, 9, 23),datetime.date(2037, 12, 23),\
               datetime.date(2038, 3, 23),datetime.date(2038, 6, 23),\
               datetime.date(2038, 9, 23),datetime.date(2038, 12, 23),\
               datetime.date(2039, 3, 23),datetime.date(2039, 6, 23),\
               datetime.date(2039, 9, 23),datetime.date(2039, 12, 23), \
               datetime.date(2040, 3, 23),datetime.date(2040, 6, 23),\
               datetime.date(2040, 9, 23),datetime.date(2040, 12, 23), \
               datetime.date(2041, 3, 23),datetime.date(2041, 6, 23),\
               datetime.date(2041, 9, 23),datetime.date(2041, 12, 23), \
               datetime.date(2042, 3, 23),datetime.date(2042, 6, 23),\
               datetime.date(2042, 9, 23),datetime.date(2042, 12, 23), \
               datetime.date(2043, 3, 23),datetime.date(2043, 6, 23),\
               datetime.date(2043, 9, 23),datetime.date(2043, 12, 23), \
               datetime.date(2044, 3, 23),datetime.date(2044, 6, 23),\
               datetime.date(2044, 9, 23),datetime.date(2044, 12, 23), \
              datetime.date(2045, 3, 23),datetime.date(2045, 6, 23),\
              datetime.date(2045, 9, 23),datetime.date(2045, 12, 23)]
                        
RequiredDatesM = {'Maturities' : pd.Series(RequiedDates)}
RequiredDatesMN = pd.DataFrame(RequiredDatesM,columns=['Maturities'])


CombDF = pd.merge(RequiredDatesMN, Observed, on='Maturities', how='outer')

#Interpolate Using Linear Methodology - Other methods can be used
InterpolatedRatesDF = CombDF.interpolate(method='polynomial', order = 3)  

interPolatedSFRDates = InterpolatedRatesDF['Maturities'].values.tolist()
interPolatedSFRRates = InterpolatedRatesDF['Observed_Rates'].values.tolist()
SFRStartingDate = datetime.date(2018, 12, 23)
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
    
discountSFRhelper(midLevelZeroRatesDates,midLevelZeroRates,1.366)


def swapRateCalculator(midLevelZeroRatesDates,midLevelZeroRates,SFRToBeBootStrapped,\
SFRDatesToBeBootStrapped):
    ans = 0.0
    ansB= 0.0
    ansC = 0.0
    ansD = 0.0
    for x in range(len(SFRToBeBootStrapped)):
        ansA = 100 -  discountSFRhelper(midLevelZeroRatesDates,midLevelZeroRates,\
        SFRToBeBootStrapped[x])
        ansB = 100+(SFRToBeBootStrapped[x])/4.0
        ansC = -1 * math.log(ansA/ansB)
        ansD = ((SFRDatesToBeBootStrapped[x] - val_date).days)/360.0
        ans = ansC / ansD
        midLevelZeroRates.append(ans)
        midLevelZeroRatesDates.append(SFRDatesToBeBootStrapped[x])
    return midLevelZeroRates

longy=[]
longy = swapRateCalculator(midLevelZeroRatesDates,midLevelZeroRates,SFRToBeBootStrapped,\
SFRDatesToBeBootStrapped)
longy2 = longy[8:]

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
    
    
RatesObserved = {'Swap_Maturities' : pd.Series(SFRDatesToBeBootStrapped),\
'Swap_Observed_Rates' : pd.Series(SFRToBeBootStrapped),'Swap_Zero_Rates' : \
pd.Series(longy2),'Swap_Discount_Rates' : pd.Series(Swap_Discount)}

Swwwap = pd.DataFrame(RatesObserved,columns=['Swap_Maturities', \
'Swap_Observed_Rates','Swap_Zero_Rates','Swap_Discount_Rates'])


midlevelMaturities = rateMaturities + rateMaturitiesFutures
Number_of_DaysMidlevel = time + numOfDaysF
Orignal_Rates = rate + ratesF
Orignal_Rates2 = [x * 100.0 for x in Orignal_Rates]
zeroRatesMidlevel = zeroRatesD + zeroRatesF
discountFactorsMidlevel =  zeroDiscounts + discFactorsFutures

Maturities = midlevelMaturities + SFRDatesToBeBootStrapped
finalRates = Orignal_Rates + SFRToBeBootStrapped
longy2 = [ x * 100.00 for x in longy2]
finalZeroRates = zeroRatesMidlevel + longy2
finalDiscount = discountFactorsMidlevel + Swap_Discount

RatesObserved = {'Maturities' : pd.Series(Maturities),\
'Rates' : pd.Series(finalRates),'Zero_Rates' : pd.Series(finalZeroRates),\
'Discount_Rates' : pd.Series(finalDiscount)}
final = pd.DataFrame(RatesObserved,columns=['Maturities', \
'Rates','Zero_Rates','Discount_Rates'])


numberOfDays = (datetime.date(2045, 12, 23) - datetime.date(2015, 12, 24)).days
elongatedMaturities = []
for x in range(1,numberOfDays+2):
    elongatedMaturities.append(val_date + timedelta(days=x))



Final3 = {'Maturities' : pd.Series(elongatedMaturities)}
Final4 = pd.DataFrame(Final3,columns=['Maturities'])

CombDF = pd.merge(Final4, final, on='Maturities', how='outer')

#Interpolate Using Linear Methodology.

InterpolatedRatesDF = CombDF.interpolate(method='polynomial', order =5)  
print
print(InterpolatedRatesDF.to_string(index=False))


"""
Preview the Final Zero Rates on a daily basis
for thirty-years:
    
Maturities        Rates   Zero_Rates  Discount_Rates
 2015-12-24  0.003674000  0.003673981     0.999989795
 2015-12-25  0.003711667  0.003711626     0.999978858
 2015-12-26  0.003749333  0.003749271     0.999967921
 2015-12-27  0.003787000  0.003786916     0.999956983
 2015-12-28  0.003824667  0.003824561     0.999946046
 2015-12-29  0.003862333  0.003862206     0.999935109
 2015-12-30  0.003900000  0.003899851     0.999924172
 2015-12-31  0.003911458  0.003911282     0.999912358
 2016-01-01  0.003922917  0.003922714     0.999900543
 2016-01-02  0.003934375  0.003934146     0.999888728

 ....................................................
 ....................................................
 ....................................................
 2045-12-16  2.607830769  2.571354083     0.457403100
 2045-12-17  2.607854945  2.571390039     0.457365343
 2045-12-18  2.607879121  2.571425995     0.457327585
 2045-12-19  2.607903297  2.571461951     0.457289827
 2045-12-20  2.607927473  2.571497907     0.457252069
 2045-12-21  2.607951648  2.571533863     0.457214311
 2045-12-22  2.607975824  2.571569819     0.457176553
 2045-12-23  2.608000000  2.571605775     0.457138795



"""

#InterpolatedRatesDF.set_index('Maturities')




import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')
import matplotlib.dates as mdates






"""
Plot the timeseries chart of the interpolated NIBOR rates and fit the observed rate.
"""

plt.close('all')
fig, ax = plt.subplots(1)
ax.plot(InterpolatedRatesDF['Maturities'],InterpolatedRatesDF['Rates'], \
lw=1.5,label='Observed/Interpolated')
fig.autofmt_xdate()
ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
plt.title('Interpolated/Observed, Zero and Discount \n \
Rates Using Cubic Spline Interpolation Method')
plt.plot(InterpolatedRatesDF['Maturities'],InterpolatedRatesDF['Zero_Rates'], 'b', \
lw=1.5,label='Zero Rates')
plt.plot(InterpolatedRatesDF['Maturities'],InterpolatedRatesDF['Discount_Rates'], 'g', \
lw=1.5,label='Discount Rates')
plt.grid(True)
plt.legend(loc=0)
plt.ylabel('Rates (%)')
plt.xlabel('Maturities')
plt.show()








    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
