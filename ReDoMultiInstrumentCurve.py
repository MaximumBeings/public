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

I think a Merry Xmas is in order - one love!!!


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
        disc_factor.append(math.exp(-1* time[x]/360.0*zeroRatesD[x]/360.0))
    return disc_factor
    
zeroDiscounts = disc_factor()



d = {'Maturities' : pd.Series(rateMaturities),'Number_of_Days' : pd.Series(time),'LIBOR_Rates' : pd.Series(rate),'Zero_Rates' : pd.Series(zeroRatesD),'Discount_Rates' : pd.Series(zeroDiscounts)}

df = pd.DataFrame(d,columns=['Maturities', 'Number_of_Days', 'LIBOR_Rates','Zero_Rates', 'Discount_Rates'])

print
print(df.to_string(index=False))

"""
The output so far look like so:
    
SHORT END
    
 Maturities  Number_of_Days  LIBOR_Rates   Zero_Rates  Discount_Rates
 2015-12-24               1    0.0036740  0.003673981     0.999999972
 2015-12-30               7    0.0039000  0.003899851     0.999999789
 2016-01-23              31    0.0041750  0.004174208     0.999999002
 2016-02-23              62    0.0050970  0.005094404     0.999997563
 2016-03-23              91    0.0059435  0.005937620     0.999995831

"""
