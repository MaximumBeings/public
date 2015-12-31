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
As can be observed from the observable data below, the rates for some dates are missing.  Hence we need to interpolate
the observable rates first then bootstrap.  For example, swap cashflows are exchanged every  quarter or semi-annually but the swap rates
are available every year from ICE - so we need to interpolate first to connect the instruments and secondly to ensure
that cashflows that fall on dates without observable rates can be discounted. So we need to first connect the rates and interpolate
then bootstrap.  It is not important to interpolate first for the short and middle area of the curve because they are available
for very short intervals but as we move out to the long end interpolation becomes important.  Interpolation can be easily
implemented in pandas.  But as I will point out later, we have to choose out data points carefully....for now lets not bother 
about that....see you next time.

Valuation Date = 2015-12-23:

Maturities        Description            Duration In Days     Type        Observed Rate     Source         
2015-12-24        Overnight              1                    Deposit     0.36740           GlobalRates.Com 
2015-12-30        One Week               7                    Deposit     0.39000           GlobalRates.Com
2016-01-23        One Month              31                   Deposit     0.41750           GlobalRates.Com 
2016-02-23        Two Months             62                   Deposit     0.50970           GlobalRates.Com
2016-03-23        Three Months           91                   Deposit     0.59435           GlobalRates.Com
2016-06-23        Six Months             183                  Futures     0.88500           CME
2016-09-23        Nine Months            275                  Futures     1.04000           CME
2016-12-23        One Year               366                  Futures     1.20000           CME
2017-03-23        One Year Three Months  456                  Futures     1.34500           CME
2017-06-23        One Year Six Months    548                  Futures     1.48500           CME
2017-09-23        One Year Nine Months   640                  Futures     1.61000           CME
2017-12-23        Two Years              731                  Futures     1.72500           CME
2018-12-23        Three Years            1096                 Swap Rate   1.36600           ICE
2019-12-23        Four Years             1461                 Swap Rate   1.54800           ICE
2020-12-23        Five Years             1826                 Swap Rate   1.69800           ICE
2021-12-23        Six Years              2191                 Swap Rate   1.82600           ICE
2022-12-23        Seven Years            2556                 Swap Rate   1.93400           ICE
2023-12-23        Eight Years            2912                 Swap Rate   2.02400           ICE
2024-12-23        Nine Years             3268                 Swap Rate   2.10200           ICE
2025-12-23        Ten Years              3633                 Swap Rate   2.17200           ICE
2030-12-23        Fifteen Years          5458                 Swap Rate   2.40700           ICE
2035-12-23        Twenty Years           7283                 Swap Rate   2.52000           ICE
2045-12-23        Thirty Years           10933                Swap Rate   2.60800           ICE


"""

"""
THE NEED FOR INTERPOLATION:  In order to be useful, we need rates to be available at least on a quarterly basis...assuming
that is the minimum cashflow duration of our instruments.  So if you look below you will realizethat there are some cashflow
payment dates without observable rates.  So we need to interpolate then bootstrap.  We are going to use different interpolation
techniques here though linear is sufficient.  Using other more complex interpolation methodologies is like taking a gun to a knife
fight....but we will cover them anyways.  And we dont have to move a muscle to use them...we have open source recipes from
scientific computing that we can use. Consider the "Not Availables" as gaps we need to fill. We already did something similar on LIBOR and NIBOR but subtle differences and different
objectives or end goal.  See next time.

Maturities        Observed Rate
2015-12-24        0.36740  
2015-12-30        0.39000
2016-01-23        0.41750
2016-02-23        0.50970
2016-03-23        0.59435
2016-06-23        0.88500
2016-09-23        1.04000
2016-12-23        1.20000
2017-03-23        1.34500
2017-06-23        1.48500
2017-09-23        1.61000
2017-12-23        1.72500
2018-03-23        Not Available
2018-06-23        Not Available
2018-09-23        Not Available
2018-12-23        1.36600
2019-03-23        Not Available
2019-06-23        Not Available
2019-09-23        Not Available
2019-12-23        1.54800
2020-03-23        Not Available
2020-06-23        Not Available
2020-09-23        Not Available
2020-12-23        1.69800
2021-03-23        Not Available
2021-06-23        Not Available
2021-09-23        Not Available
2021-12-23        1.82600
2022-03-23        Not Available
2022-06-23        Not Available
2022-09-23        Not Available
2022-12-23        1.93400
2023-03-23        Not Available
2023-06-23        Not Available
2023-09-23        Not Available
2023-12-23        2.02400
2024-03-23        Not Available
2024-06-23        Not Available
2024-09-23        Not Available
2024-12-23        2.10200
2025-03-23        Not Available
2025-06-23        Not Available
2025-09-23        Not Available
2025-12-23        2.17200
2026-03-23        Not Available
2026-06-23        Not Available
2026-09-23        Not Available
2026-12-23        Not Available
2027-03-23        Not Available
2027-06-23        Not Available
2027-09-23        Not Available
2027-12-23        Not Available
2028-03-23        Not Available
2028-06-23        Not Available
2028-09-23        Not Available
2028-12-23        Not Available
2029-03-23        Not Available
2029-06-23        Not Available
2029-09-23        Not Available
2029-12-23        Not Available
2030-03-23        Not Available
2030-06-23        Not Available
2030-09-23        Not Available
2030-12-23        2.40700
2031-03-23        Not Available
2031-06-23        Not Available
2031-09-23        Not Available
2031-12-23        Not Available
2032-03-23        Not Available
2032-06-23        Not Available
2032-09-23        Not Available
2032-12-23        Not Available
2033-03-23        Not Available
2033-06-23        Not Available
2033-09-23        Not Available
2033-12-23        Not Available
2034-03-23        Not Available
2034-06-23        Not Available
2034-09-23        Not Available
2034-12-23        Not Available
2035-03-23        Not Available
2035-06-23        Not Available
2035-09-23        Not Available
2035-12-23        2.52000
2036-03-23        Not Available
2036-06-23        Not Available
2036-09-23        Not Available
2036-12-23        Not Available
2037-03-23        Not Available
2037-06-23        Not Available
2037-09-23        Not Available
2037-12-23        Not Available
2038-03-23        Not Available
2038-06-23        Not Available
2038-09-23        Not Available
2038-12-23        Not Available
2039-03-23        Not Available
2039-06-23        Not Available
2039-09-23        Not Available
2039-12-23        Not Available
2040-03-23        Not Available
2040-06-23        Not Available
2040-09-23        Not Available
2040-12-23        Not Available
2041-03-23        Not Available
2041-06-23        Not Available
2041-09-23        Not Available
2041-12-23        Not Available
2042-03-23        Not Available
2042-06-23        Not Available
2042-09-23        Not Available
2042-12-23        Not Available
2043-03-23        Not Available
2043-06-23        Not Available
2043-09-23        Not Available
2043-12-23        Not Available
2044-03-23        Not Available
2044-06-23        Not Available
2044-09-23        Not Available
2044-12-23        Not Available
2045-03-23        Not Available
2045-06-23        Not Available
2045-09-23        Not Available
2045-12-23        2.60800
  

"""

"""
REPRESENTATION OF OBSERVED RATES:
    
Maturities  Observed_Rates
 2015-12-24         0.36740
 2015-12-30         0.39000
 2016-01-23         0.41750
 2016-02-23         0.50970
 2016-03-23         0.59435
 2016-06-23         0.88500
 2016-09-23         1.04000
 2016-12-23         1.20000
 2017-03-23         1.34500
 2017-06-23         1.48500
 2017-09-23         1.61000
 2017-12-23         1.72500
 2018-12-23         1.36600
 2019-12-23         1.54800
 2020-12-23         1.69800
 2021-12-23         1.82600
 2022-12-23         1.93400
 2023-12-23         2.02400
 2024-12-23         2.10200
 2025-12-23         2.17200
 2030-12-23         2.40700
 2035-12-23         2.52000
 2045-12-23         2.60800

"""

"""
REPRESENTATION OF MATURITIES:

Maturities
 2015-12-24
 2015-12-30
 2016-01-23
 2016-02-23
 2016-03-23
 2016-06-23
 2016-09-23
 2016-12-23
 2017-03-23
 2017-06-23
 2017-09-23
 2017-12-23
 2018-03-23
 2018-06-23
 2018-09-23
 2018-12-23
 2019-03-23
 2019-06-23
 2019-09-23
 2019-12-23
 2020-03-23
 2020-06-23
 2020-09-23
 2020-12-23
 2021-03-23
 2021-06-23
 2021-09-23
 2021-12-23
 2022-03-23
 2022-06-23
 2022-09-23
 2022-12-23
 2023-03-23
 2023-06-23
 2023-09-23
 2023-12-23
 2024-03-23
 2024-06-23
 2024-09-23
 2024-12-23
 2025-03-23
 2025-06-23
 2025-09-23
 2025-12-23
 2026-03-23
 2026-06-23
 2026-09-23
 2026-12-23
 2027-03-23
 2027-06-23
 2027-09-23
 2027-12-23
 2028-03-23
 2028-06-23
 2028-09-23
 2028-12-23
 2029-03-23
 2029-06-23
 2029-09-23
 2029-12-23
 2030-03-23
 2030-06-23
 2030-09-23
 2030-12-23
 2031-03-23
 2031-06-23
 2031-09-23
 2031-12-23
 2032-03-23
 2032-06-23
 2032-09-23
 2032-12-23
 2033-03-23
 2033-06-23
 2033-09-23
 2033-12-23
 2034-03-23
 2034-06-23
 2034-09-23
 2034-12-23
 2035-03-23
 2035-06-23
 2035-09-23
 2035-12-23
 2036-03-23
 2036-06-23
 2036-09-23
 2036-12-23
 2037-03-23
 2037-06-23
 2037-09-23
 2037-12-23
 2038-03-23
 2038-06-23
 2038-09-23
 2038-12-23
 2039-03-23
 2039-06-23
 2039-09-23
 2039-12-23
 2040-03-23
 2040-06-23
 2040-09-23
 2040-12-23
 2041-03-23
 2041-06-23
 2041-09-23
 2041-12-23
 2042-03-23
 2042-06-23
 2042-09-23
 2042-12-23
 2043-03-23
 2043-06-23
 2043-09-23
 2043-12-23
 2044-03-23
 2044-06-23
 2044-09-23
 2044-12-23
 2045-03-23
 2045-06-23
 2045-09-23
 2045-12-23

"""

"""
COMBINATION OF OBSERVED WITH REQUIRED MATURITIES WITHOUT INTERPOLATION NaN = Null and are required to be filled:
    
Maturities  Observed_Rates
 2015-12-24         0.36740
 2015-12-30         0.39000
 2016-01-23         0.41750
 2016-02-23         0.50970
 2016-03-23         0.59435
 2016-06-23         0.88500
 2016-09-23         1.04000
 2016-12-23         1.20000
 2017-03-23         1.34500
 2017-06-23         1.48500
 2017-09-23         1.61000
 2017-12-23         1.72500
 2018-03-23             NaN
 2018-06-23             NaN
 2018-09-23             NaN
 2018-12-23         1.36600
 2019-03-23             NaN
 2019-06-23             NaN
 2019-09-23             NaN
 2019-12-23         1.54800
 2020-03-23             NaN
 2020-06-23             NaN
 2020-09-23             NaN
 2020-12-23         1.69800
 2021-03-23             NaN
 2021-06-23             NaN
 2021-09-23             NaN
 2021-12-23         1.82600
 2022-03-23             NaN
 2022-06-23             NaN
 2022-09-23             NaN
 2022-12-23         1.93400
 2023-03-23             NaN
 2023-06-23             NaN
 2023-09-23             NaN
 2023-12-23         2.02400
 2024-03-23             NaN
 2024-06-23             NaN
 2024-09-23             NaN
 2024-12-23         2.10200
 2025-03-23             NaN
 2025-06-23             NaN
 2025-09-23             NaN
 2025-12-23         2.17200
 2026-03-23             NaN
 2026-06-23             NaN
 2026-09-23             NaN
 2026-12-23             NaN
 2027-03-23             NaN
 2027-06-23             NaN
 2027-09-23             NaN
 2027-12-23             NaN
 2028-03-23             NaN
 2028-06-23             NaN
 2028-09-23             NaN
 2028-12-23             NaN
 2029-03-23             NaN
 2029-06-23             NaN
 2029-09-23             NaN
 2029-12-23             NaN
 2030-03-23             NaN
 2030-06-23             NaN
 2030-09-23             NaN
 2030-12-23         2.40700
 2031-03-23             NaN
 2031-06-23             NaN
 2031-09-23             NaN
 2031-12-23             NaN
 2032-03-23             NaN
 2032-06-23             NaN
 2032-09-23             NaN
 2032-12-23             NaN
 2033-03-23             NaN
 2033-06-23             NaN
 2033-09-23             NaN
 2033-12-23             NaN
 2034-03-23             NaN
 2034-06-23             NaN
 2034-09-23             NaN
 2034-12-23             NaN
 2035-03-23             NaN
 2035-06-23             NaN
 2035-09-23             NaN
 2035-12-23         2.52000
 2036-03-23             NaN
 2036-06-23             NaN
 2036-09-23             NaN
 2036-12-23             NaN
 2037-03-23             NaN
 2037-06-23             NaN
 2037-09-23             NaN
 2037-12-23             NaN
 2038-03-23             NaN
 2038-06-23             NaN
 2038-09-23             NaN
 2038-12-23             NaN
 2039-03-23             NaN
 2039-06-23             NaN
 2039-09-23             NaN
 2039-12-23             NaN
 2040-03-23             NaN
 2040-06-23             NaN
 2040-09-23             NaN
 2040-12-23             NaN
 2041-03-23             NaN
 2041-06-23             NaN
 2041-09-23             NaN
 2041-12-23             NaN
 2042-03-23             NaN
 2042-06-23             NaN
 2042-09-23             NaN
 2042-12-23             NaN
 2043-03-23             NaN
 2043-06-23             NaN
 2043-09-23             NaN
 2043-12-23             NaN
 2044-03-23             NaN
 2044-06-23             NaN
 2044-09-23             NaN
 2044-12-23             NaN
 2045-03-23             NaN
 2045-06-23             NaN
 2045-09-23             NaN
 2045-12-23         2.60800

"""

"""
COMBINATION OF OBSERVED WITH REQUIRED MATURITIES WITHOUT INTERPOLATION:
    
Maturities  Observed_Rates
 2015-12-24         0.36740
 2015-12-30         0.39000
 2016-01-23         0.41750
 2016-02-23         0.50970
 2016-03-23         0.59435
 2016-06-23         0.88500
 2016-09-23         1.04000
 2016-12-23         1.20000
 2017-03-23         1.34500
 2017-06-23         1.48500
 2017-09-23         1.61000
 2017-12-23         1.72500
 2018-03-23         1.63525
 2018-06-23         1.54550
 2018-09-23         1.45575
 2018-12-23         1.36600
 2019-03-23         1.41150
 2019-06-23         1.45700
 2019-09-23         1.50250
 2019-12-23         1.54800
 2020-03-23         1.58550
 2020-06-23         1.62300
 2020-09-23         1.66050
 2020-12-23         1.69800
 2021-03-23         1.73000
 2021-06-23         1.76200
 2021-09-23         1.79400
 2021-12-23         1.82600
 2022-03-23         1.85300
 2022-06-23         1.88000
 2022-09-23         1.90700
 2022-12-23         1.93400
 2023-03-23         1.95650
 2023-06-23         1.97900
 2023-09-23         2.00150
 2023-12-23         2.02400
 2024-03-23         2.04350
 2024-06-23         2.06300
 2024-09-23         2.08250
 2024-12-23         2.10200
 2025-03-23         2.11950
 2025-06-23         2.13700
 2025-09-23         2.15450
 2025-12-23         2.17200
 2026-03-23         2.18375
 2026-06-23         2.19550
 2026-09-23         2.20725
 2026-12-23         2.21900
 2027-03-23         2.23075
 2027-06-23         2.24250
 2027-09-23         2.25425
 2027-12-23         2.26600
 2028-03-23         2.27775
 2028-06-23         2.28950
 2028-09-23         2.30125
 2028-12-23         2.31300
 2029-03-23         2.32475
 2029-06-23         2.33650
 2029-09-23         2.34825
 2029-12-23         2.36000
 2030-03-23         2.37175
 2030-06-23         2.38350
 2030-09-23         2.39525
 2030-12-23         2.40700
 2031-03-23         2.41265
 2031-06-23         2.41830
 2031-09-23         2.42395
 2031-12-23         2.42960
 2032-03-23         2.43525
 2032-06-23         2.44090
 2032-09-23         2.44655
 2032-12-23         2.45220
 2033-03-23         2.45785
 2033-06-23         2.46350
 2033-09-23         2.46915
 2033-12-23         2.47480
 2034-03-23         2.48045
 2034-06-23         2.48610
 2034-09-23         2.49175
 2034-12-23         2.49740
 2035-03-23         2.50305
 2035-06-23         2.50870
 2035-09-23         2.51435
 2035-12-23         2.52000
 2036-03-23         2.52220
 2036-06-23         2.52440
 2036-09-23         2.52660
 2036-12-23         2.52880
 2037-03-23         2.53100
 2037-06-23         2.53320
 2037-09-23         2.53540
 2037-12-23         2.53760
 2038-03-23         2.53980
 2038-06-23         2.54200
 2038-09-23         2.54420
 2038-12-23         2.54640
 2039-03-23         2.54860
 2039-06-23         2.55080
 2039-09-23         2.55300
 2039-12-23         2.55520
 2040-03-23         2.55740
 2040-06-23         2.55960
 2040-09-23         2.56180
 2040-12-23         2.56400
 2041-03-23         2.56620
 2041-06-23         2.56840
 2041-09-23         2.57060
 2041-12-23         2.57280
 2042-03-23         2.57500
 2042-06-23         2.57720
 2042-09-23         2.57940
 2042-12-23         2.58160
 2043-03-23         2.58380
 2043-06-23         2.58600
 2043-09-23         2.58820
 2043-12-23         2.59040
 2044-03-23         2.59260
 2044-06-23         2.59480
 2044-09-23         2.59700
 2044-12-23         2.59920
 2045-03-23         2.60140
 2045-06-23         2.60360
 2045-09-23         2.60580
 2045-12-23         2.60800

"""


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
 2015-12-24               1    0.0036740  0.003673981     0.999989795
 2015-12-30               7    0.0039000  0.003899851     0.999924172
 2016-01-23              31    0.0041750  0.004174208     0.999640619
 2016-02-23              62    0.0050970  0.005094404     0.999123015
 2016-03-23              91    0.0059435  0.005937620     0.998500227


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
