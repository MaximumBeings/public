"""
Topic: Multi Instrument Swap Curve Construction

Source: Ron Uri - A Practical Guide to Swap Curve Contruction - Bank of Canada (Google it).

Discussion:  To develop a multi-instrument swap curve construction program in python per the above article.  Excluding
the effect of convexity adjustment which will be addressed at a later time.  Program is a prototype and not working
properly.  We will revisit shortly and rewrite the program from the top.  Posted as a work-in-progress.  It will be a great 
addition to our yield curve library when fully done. See you next time.

*****NOT WORKING PROPERLY - FOR PROTOTYPING PURPOSES ONLY - TO BE UPDATED*********
"""



"""
USD LIBOR - Overnight       0.09340%
USD LIBOR - 1 Week          0.12250%
USD LIBOR - 1 Month         0.15200%
USD LIBOR - 2 Months        0.19275%
USD LIBOR - 3 Months        0.23260%
"""

import datetime
import pandas as pd
from dateutil.relativedelta import relativedelta
from datetime import date, timedelta
import locale
import math
locale.setlocale(locale.LC_ALL, '')

val_date = datetime.date(2014, 1, 1)
rate = [0.09340/100.0,0.12250/100.0,0.15200/100.0,0.19275/100.0,0.23260/100.0]
rateMaturities = [val_date + timedelta(days=1),val_date + timedelta(weeks=1),val_date + relativedelta(months=1),val_date+relativedelta(months=2),val_date+relativedelta(months=3)]
rateMatInDays = []
def rateMatInDaysFunctn(val_date, rateMaturities):
    for x in range(len(rateMaturities)):
        rateMatInDays.append((rateMaturities[x] - val_date).days)
    return rateMatInDays

#rateMatInDays = []  
#rateMatInDays = rateMatInDaysFunctn(val_date, rateMaturities)

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
def deepcopy(A):
    rt = []
    for elem in A:
        if isinstance(elem,list):
            rt.append(deepcopy(elem))
        else:
            rt.append(elem)
    return rt
    
ty = 360  #day count convention
def zeroRateDeposits(ty, rate, rateMatInDays):
    rc = []
    for x in range(len(rateMatInDays)):
        rc.append((ty/rateMatInDays[x]) * math.log(1 + rate[x]/(ty/rateMatInDays[x])))
    return rc


time = deepcopy(rateMatInDaysFunctn(val_date, rateMaturities))
zeroRatesD = deepcopy(zeroRateDeposits(ty, rate, rateMatInDays))

def disc_factor():
    #Using the zero rates calculated above we calculate our discount factors as documented below.
    #This program returns a vector of discount factors for the different cashflow payments
    disc_factor = []
    for x in range(len(time)):
        disc_factor.append(math.exp(-1* time[x]/360.0*zeroRatesD[x]/360.0))
    return disc_factor
        

"""
THE MIDDLE AREA OF THE SWAP CURVE:
    
Futures Prices for June 30, Sept 30 and Dec 31, 2014 (Assumed)
June 30th, 2014             99.760
Sept 30th, 2014             99.730
Dec  31st, 2014             99.635
Mar 31st, 2015              99.645
June 30th, 2015             99.470
Sept 30th, 2015             99.255
Dec 31st, 2015              99.025

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

futurePrices = [99.760,99.730,99.635,99.645,99.470,99.255,99.025]
#The first step is to convert the futures prices into future interest rate using the above formula


def futureInterestRate(futurePrices):
    fInterestRate = []
    for x in range(len(futurePrices)):
        fInterestRate.append((futurePrices[x] - 100.0)/(-1*100.0))
    return fInterestRate
    
ratesF = deepcopy(futureInterestRate(futurePrices))
    
rateMaturitiesFutures = [val_date + relativedelta(months=6),val_date+relativedelta(months=9),val_date+relativedelta(months=12), \
                 val_date + relativedelta(months=15),val_date+relativedelta(months=18),val_date+relativedelta(months=21),
                 val_date + relativedelta(months=24)]
                 
lastDepositDate = datetime.date(2014, 4, 1)  #3 months from January 1, 2014


rateMatInDaysFutures = []
def rateDaysFurtures(val_date, rateMaturitiesFutures):
    for x in range(len(rateMaturitiesFutures)):
        rateMatInDaysFutures.append((rateMaturitiesFutures[x] - val_date).days)
        
    return rateMatInDaysFutures

numOfDaysF = deepcopy(rateDaysFurtures(val_date, rateMaturitiesFutures))
ty = float(360)  #day count convention

lastDepositDate2 = (datetime.date(2014, 4, 1) - val_date).days

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

ContFuture = deepcopy(contCompFuturesRate(ty, ratesF, numOfDaysF))

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
            
zeroRatesF = deepcopy(zeroRateFutures(numOfDaysF, ContFuture,time,zeroRatesD))

#Discount Factors for Futures Rate
def disc_factor_2():
    #Using the zero rates calculated above we calculate our discount factors as documented below.
    #This program returns a vector of discount factors for the different cashflow payments
    disc_factor = []
    for x in range(len(numOfDaysF)):
        disc_factor.append(math.exp(-1* numOfDaysF[x]/360.0*zeroRatesF[x]/360.0))
    return disc_factor
    
"""
THE LONG-END OF THE SWAP CURVE:
    
Swap Fixed Rates up to 5 years assumed (Assumed)
Mar 31st, 2016              0.66
Jun 30th, 2016              0.75
Sept 30th 2016              0.99
Dec 31st 2016               1.52
Mar 31st, 2017              1.75
Jun 30th, 2017              1.99
Sept 30th 2017              2.30
Dec 31st 2017               2.75
Mar 31st, 2018              3.00
Jun 30th, 2018              3.33
Sept 30th 2018              3.80
Dec 31st 2018               4.10


The long end of the swap curve out to ten years is derived directly from
observable coupon swap rates.  These are generic plain vanilla interest
rate swaps with fixed rates exchanged for floating interest rates. The
fixed swap rates are quoted as par rates and are usually compounded semi-
annually...We have discussed bootstrapping and interpolation methodology but 
this one is in continuous time.


"""

val_date = datetime.date(2014, 1, 1)
swap_rate_dates = [datetime.date(2016, 3, 31),datetime.date(2016, 6, 30),datetime.date(2016, 9, 30),datetime.date(2016, 12, 31), \
                  datetime.date(2017, 3, 31),datetime.date(2017, 6, 30),datetime.date(2017, 9, 30),datetime.date(2017, 12, 31), \
                  datetime.date(2018, 3, 31),datetime.date(2018, 6, 30),datetime.date(2018, 9, 30),datetime.date(2018, 12, 31)]
compounding = 3
numOfQuartersInFiveYears = 60/4 
def maturities(val_date,compounding):
    maturities = []
    for y in range(1,numOfQuartersInFiveYears):
        maturities.append((val_date)+relativedelta(months=compounding*y))
    return maturities
    
swapCashFlowDates = deepcopy(maturities(val_date,compounding))
swapFixedRates = [0.66/100,0.75/100,0.99/100,1.52/100,1.75/100,1.99/100,2.30/100,2.75/100,3.00/100,3.33/100,3.80/100,4.10/100]


#Combine the zero rates we previously calculated.

combinedZeroRates = zeroRatesD+ zeroRatesF
combinedZeroDates = time + numOfDaysF
combinedZeroRates=combinedZeroRates[4:]  #Becos interest payments on a swap occur every three months in this case we only want info from the third month
combinedZeroDates=combinedZeroDates[4:]  #Becos interest payments on a swap occur every three months in this case we only want info from the third month

def discountSFRhelper(dater,val_date,combiner):
    final = 0.0
    ans = 0.0
    n = (dater - val_date).days/90
    for x in range(n):
        numberOfDays = (swapCashFlowDates[x] - val_date).days
        ans = swapFixedRates[x]/4.0 * math.exp(-1*combiner[x]*numberOfDays)
        final = final + ans
    return final

combiner = deepcopy(combinedZeroRates)
#Function to calculate Swap Fixed Rate
def swapRateCalculator():
    
    ans = 0.0
    for x in range(len(swapFixedRates)):
        ans = 100 -  discountSFRhelper(swapCashFlowDates[x],val_date,combiner)
        ans = -1 * math.log(ans/(100+swapFixedRates[x]/4.0))
        combiner.append(ans)
    return combiner



full_date = rateMaturities + rateMaturitiesFutures +  swap_rate_dates
full_zero_rates = zeroRatesD + zeroRatesF + swapRateCalculator()[8:]

rateTable = pd.DataFrame.from_items([('Period', range(1,25,1)),('full_date', full_date), ('full_zero_rates', full_zero_rates)])
print(rateTable.to_string())


"""
FINAL OUTPUT:
    Period   full_date  full_zero_rates
0        1  2014-01-02         0.000934
1        2  2014-01-08         0.001225
2        3  2014-02-01         0.001520
3        4  2014-03-01         0.001927
4        5  2014-04-01         0.002325
5        6  2014-07-01         0.002363
6        7  2014-10-01         0.002476
7        8  2015-01-01         0.002771
8        9  2015-04-01         0.002925
9       10  2015-07-01         0.003320
10      11  2015-10-01         0.003915
11      12  2016-01-01         0.004649
12      13  2016-03-31         0.000030
13      14  2016-06-30         0.000044
14      15  2016-09-30         0.000063
15      16  2016-12-31         0.000090
16      17  2017-03-31         0.000107
17      18  2017-06-30         0.000121
18      19  2017-09-30         0.000134
19      20  2017-12-31         0.000147
20      21  2018-03-31         0.000227
21      22  2018-06-30         0.000315
22      23  2018-09-30         0.000416
23      24  2018-12-31         0.000517

"""
