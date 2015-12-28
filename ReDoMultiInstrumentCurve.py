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
the effect of convexity adjustment which will be addressed at a later time.  I was developing this model last year and I need to fix 
some parts of the codes that are not working correctly.  I will test it in Excel....reperform everything in excel to make sure it is working okay.
Usually, I dont do that but this article does not have numbers to benchmark against just formulae so I need to go that extra mile.  I usually
avoid articles without solution when I am modeling because I have to go the extra mile to double check that the model is working correctly.
Whereas, if it had solutions, my work is cut in half.  That aside, great article.  Swap curves can be used as benchmark reference rate for valuing
different fixed income instrumnents.

The original one can be found here - https://github.com/MaximumBeings/public/blob/master/multiInstrumentSwapCurve.py

I think a Merry Xmas is in order - one love!!!....Mid area completed and long end remainining. Incomplete codes posted to github.
Long end will be completed shortly


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
rateMaturities = [val_date + timedelta(days=1),val_date + timedelta(weeks=1),val_date + relativedelta(months=1),val_date+relativedelta(months=2),val_date+relativedelta(months=3)]

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

print
print(df.to_string(index=False))

"""
The output so far look like so:
    
 Maturities  Number_of_Days  LIBOR_Rates   Zero_Rates  Discount_Rates
 2015-12-24               1    0.0036740  0.003673981     0.999999972
 2015-12-30               7    0.0039000  0.003899851     0.999999789
 2016-01-23              31    0.0041750  0.004174208     0.999999002
 2016-02-23              62    0.0050970  0.005094404     0.999997563
 2016-03-23              91    0.0059435  0.005937620     0.999995831

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

futurePrices = [99.115,98.960,98.800,98.655,98.515,98.390,98.275]
#The first step is to convert the futures prices into future interest rate using the above formula


def futureInterestRate(futurePrices):
    fInterestRate = []
    
    
ratesF = copy.deepcopy(futureInterestRate(futurePrices))
    
rateMaturitiesFutures = [datetime.date(2016, 6, 30),datetime.date(2016, 9, 30),datetime.date(2016, 12, 31),datetime.date(2017, 3, 31), \
                        datetime.date(2017, 6, 30),datetime.date(2017, 9, 30),datetime.date(2017, 12, 31)]
                 
lastDepositDate = datetime.date(2016, 3, 23)  



def rateDaysFurtures(val_date, rateMaturitiesFutures):
    rateMatInDaysFutures = []
   
        
    return rateMatInDaysFutures

numOfDaysF = copy.deepcopy(rateDaysFurtures(val_date, rateMaturitiesFutures))

ty = float(360)  #day count convention

lastDepositDate2 = (datetime.date(2016, 3, 23) - val_date).days

def contCompFuturesRate(ty, ratesF, numOfDaysF):
    rc = []
    
    for x in range(len(numOfDaysF)):
      
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
    
    return disc_factor

discFactorsFutures = disc_factor_2()
    
midlevelMaturities = rateMaturities + rateMaturitiesFutures
Number_of_DaysMidlevel = time + numOfDaysF
Orignal_Rates = rate + ratesF
Orignal_Rates2 = [x * 100 for x in Orignal_Rates]
zeroRatesMidlevel = zeroRatesD + zeroRatesF
discountFactorsMidlevel =  zeroDiscounts + discFactorsFutures
Instrument = ["Deposit", "Deposit", "Deposit","Deposit", "Deposit","Futures", "Futures","Futures","Futures","Futures","Futures","Futures"]




"""
MID-LEVEL RATES:
    
 Maturities  Number_of_Days Instrument  Original_Rates_(%)   Zero_Rates  Discount_Rates
 2015-12-24               1    Deposit             0.36740  0.003673981     0.999989795
 2015-12-30               7    Deposit             0.39000  0.003899851     0.999924172
 2016-01-23              31    Deposit             0.41750  0.004174208     0.999640619
 2016-02-23              62    Deposit             0.50970  0.005094404     0.999123015
 2016-03-23              91    Deposit             0.59435  0.005937620     0.998500227
 2016-06-30             190    Futures             0.88500  0.007449521     0.996076027
 2016-09-30             282    Futures             1.04000  0.008407588     0.993435696
 2016-12-31             374    Futures             1.20000  0.009286766     0.990398474
 2017-03-31             464    Futures             1.34500  0.010089913     0.987079419
 2017-06-30             555    Futures             1.48500  0.010865838     0.983388027
 2017-09-30             647    Futures             1.61000  0.011605411     0.979358510
 2017-12-31             739    Futures             1.72500  0.012303401     0.975060120

"""