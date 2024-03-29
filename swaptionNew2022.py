from __future__ import division
from math import exp, sqrt
from scipy.optimize import fsolve
import math
import sys
import copy
import scipy.stats
import datetime
import pandas as pd
from dateutil.relativedelta import relativedelta
import locale
locale.setlocale(locale.LC_ALL, '')
import locale




"""
Year        Swap_Rate_YTM        Coupon
0.5         8.8700               0.04435
1           9.0400               0.04520
1.5         9.1550               0.04578
2           9.2700               0.04635
2.5         9.3150               0.04658
3           9.3600               0.04680
3.5         9.3850               0.04693
4           9.4100               0.04705
4.5         9.4350               0.04718
5           9.4600               0.04730
5.5         9.4700               0.04735
6           9.4800               0.04740
6.5         9.4900               0.04745
7           9.5000               0.04750
              
"""
def boostrapHelper(gUESS,tIME,yTM,sPOT):
    collector = 0.0
    rate2=[]
    rate=[]
    for x in range(len(tIME)):            
        if x == len(tIME) - 1:
            y = yTM[0]
            g = gUESS[0]
            t = tIME[x]
            collector = ((100 + y/2.0)/(1+g/2.0)**(t*2))
            rate.append(collector)
        else:
            y = yTM[0]
            s = sPOT[x]
            t = tIME[x]
            collector = ((y/2.0)/(1+s/2.0)**(t*2))
            rate.append(collector)
        collector = 0.0
        rate2=rate[:]
            
    return (100- sum(rate2))
    
tIME = [0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7]
yTM = [8.8700, 9.0400,9.155,9.2700,9.3150,9.3600,9.3850,9.4100,9.4350,9.4600,9.4700,9.4800,9.4900,9.5000]
gUESS = [0.12]
#yTM = [9.155]
#
#sPOT=[]
#sPOT.append(yTM1[0]/100)
#sPOT = [0.08869999999999999,0.090438452331122077]

#
#data = ([0.5,1,1.5], [9.155])
#fsolve(boostrapHelper,gUESS,args=data)[0]

def bootStrapper(tIME, yTM, gUESS):
    sPOT=[]
    
    for x in range(len(tIME)):
        if x == 0:
            sPOT.append(yTM[0]/100)
        else:
            tIME2 = tIME[:x+1]
            yTM2 = [yTM[x]]
            data = (tIME2,yTM2,sPOT)

            sPOT.append(fsolve(boostrapHelper,gUESS,args=data)[0])

    return sPOT
        
"""
Calculate Discount Rate from Zero Rates
"""

zeroRates = bootStrapper(tIME, yTM, gUESS)



def discountFactorCalculator(zeroRates,tIME):
    discountRates = []
    for x in range(len(zeroRates)):
        discountRates.append(1/((1+zeroRates[x]/2.0)**(tIME[x]*2)))
    return discountRates
        
discountFactors = discountFactorCalculator(zeroRates,tIME)


def futureValueCurve(discountFactors):
    futureValueCurve = []
    for x in range(len(discountFactors)):
        futureValueCurve.append(1/discountFactors[x])
    return futureValueCurve
    
futureValueCurve = futureValueCurve(discountFactors)

def forwardRateCurve(futureValueCurve):
    forwardRateCurve = []
    for x in range(len(futureValueCurve)):
        if x == 0:
            forwardRateCurve.append(zeroRates[0])
        else:
            forwardRateCurve.append((((futureValueCurve[x]/futureValueCurve[x-1])**(1/(0.5*2))) - 1)*2)
    return forwardRateCurve

forwardRateCurve = forwardRateCurve(futureValueCurve)

def forwardRateCurve2(zeroRates,tIME):
    forwardRateCurve2 = []
    for x in range(len(zeroRates)):
        if x == 0:
            forwardRateCurve2.append(zeroRates[0])
        else:
            a =(1+zeroRates[x]/2)**(tIME[x]*2)
            b =(1+zeroRates[x-1]/2)**(tIME[x-1]*2)
            c = a**(0.5*2)/b**(0.5*2)
            d = c**(1/(0.5*2))
            e = d -1
            f = e * 2
            forwardRateCurve2.append(f)
    return forwardRateCurve2

forwardRateCurve2 = forwardRateCurve2(zeroRates,tIME)


def annualSpotRate(zeroRates):
    annualSpotRate = []
    for x in range(len(zeroRates)): 
        annualSpotRate.append((1 + zeroRates[x]/2)**2 - 1)
    
    return annualSpotRate


annualSpotRate = annualSpotRate(zeroRates)




import pandas as pd

d = {'Time' : pd.Series(tIME),'YTM' : pd.Series(yTM),'Spot Rates' : pd.Series(zeroRates),'Disc_Factors' : pd.Series(discountFactors), \
    'Future_Value' : pd.Series(futureValueCurve),'Forward_Rate_Version_1' : pd.Series(forwardRateCurve), \
    'Forward_Rate_Version_2' : pd.Series(forwardRateCurve2), 'Annual_Spot_Rate' : pd.Series(annualSpotRate)}

print

df = pd.DataFrame(d,columns=['Time', 'YTM', 'Spot Rates','Annual_Spot_Rate','Disc_Factors','Future_Value','Forward_Rate_Version_1','Forward_Rate_Version_2'])

print(df.to_string())


"""
OUTPUT


    Time    YTM  Spot Rates  Disc_Factors  Future_Value  Forward_Rate_Version_1  Forward_Rate_Version_2  Annual_Spot_Rate
0    0.5  8.870    0.088700      0.957533      1.044350                0.088700                0.088700          0.090667
1    1.0  9.040    0.090438      0.915346      1.092483                0.092178                0.092178          0.092483
2    1.5  9.155    0.091629      0.874250      1.143837                0.094014                0.094014          0.093728
3    2.0  9.270    0.092843      0.834014      1.199021                0.096488                0.096488          0.094998
4    2.5  9.315    0.093309      0.796129      1.256079                0.095174                0.095174          0.095486
5    3.0  9.360    0.093789      0.759595      1.316492                0.096193                0.096193          0.095989
6    3.5  9.385    0.094051      0.724935      1.379434                0.095621                0.095621          0.096263
7    4.0  9.410    0.094322      0.691660      1.445798                0.096219                0.096219          0.096546
8    4.5  9.435    0.094601      0.659718      1.515799                0.096833                0.096833          0.096838
9    5.0  9.460    0.094887      0.629062      1.589668                0.097467                0.097467          0.097138
10   5.5  9.470    0.094989      0.600248      1.665978                0.096006                0.096006          0.097245
11   6.0  9.480    0.095096      0.572681      1.746173                0.096274                0.096274          0.097357
12   6.5  9.490    0.095208      0.546308      1.830470                0.096550                0.096550          0.097474
13   7.0  9.500    0.095324      0.521079      1.919096                0.096835                0.096835          0.097596


"""


def forwardRateCalculator(zeroRates,sTART,sTOP):
    sTOP = 7
    sTART = 5
    a =(1+zeroRates[sTOP*2-1]/2)**(sTOP*2)
    b =(1+zeroRates[sTART*2-1]/2)**(sTART*2)
    c = a/b
    d = c**(1.0/(2*2))
    e = d -1
    f = e * 2
    return f

forwardRateCalculator = forwardRateCalculator(zeroRates,5,7)

print
print ("The 7 year forward rate starting  in year 5 is %s " % forwardRateCalculator)


"""
EXAMPLE:  Consider, as an example, a forward semi-annual swap beginning five years from now and having a term of two years
(i.e., ending in seven years). A forward swap beginning in five years for a term of two years is conventionally described as a 
"seven/five" swap.  For a seven/five forward swap, the forward rate is as calculated above.  This rate becomes the underlying
security price for the "Black 76" commodity option model.  The model uses the following input

(a) the forward rate as the underlying price
(b) the swaption strike as the exercise price
(c) the spot rate at the expiration date of the swaption as the interest rate and
(d) an implied volatility specified by the user.
"""

Settlement_Date = datetime.date(1990, 3, 14)
Maturity_Date = datetime.date(1995, 3, 14)
t = (Maturity_Date - Settlement_Date).days
SP = 9.6416/100.0 # Underlying Security Price or the Forward Rate starting in year 5 and ending in year 7
EP = 9.500/100.0 #Exercise Price or Swaption Strike
r = 9.4887/100.0 #Spot Rate in Year 5 when the option expires and the forward swap kicks in
v = 11.0/100.0 #implied volatility chosen by user
# N = Normal Cumulative Density Function
# D = Delta = N(d1) for calls and N(d2) for puts

#implement a function to calculate Cumulative Density Function

def cumm_dens_function_scipy(t):
    return scipy.stats.norm.cdf(t)


def blackSeventySix(SP,EP,r,v,t):
    d1 = (math.log(SP/EP) + (0.5 * v * v * t/365.0))/(v * math.sqrt(t/365.0))
    d2 = d1 - v * math.sqrt(t/365.0)
    ND1 = cumm_dens_function_scipy(d1)
    ND2 = cumm_dens_function_scipy(d2)
    call_Value = (SP * ND1 - EP * ND2) * ( 1 + 0.5* r)**(t/(-365.0/2)) * 100.0
    put_Value = call_Value - (SP - EP) * ( 1 + 0.5* r)**(t/(-365.0/2)) * 100.0
    result = {'call': call_Value, 'put': put_Value}
    return result

print()

print(blackSeventySix(SP,EP,r,v,t))

#{'put': 0.54584416243351719, 'call': 0.63489682074640741}


#result = blackSeventySix(SP,EP,r,v,t)
#
#for key, value in result.iteritems():
#    print key, value

"""
IMPORTANT NOTES FROM THE JOURNAL:
Because the option is on a forward rate (the forward spot rate), the call option derived from the model benefits
when the forward rate rises while the put option benefits when the forward rate falls. In practice, swaptions are defined
in line with bond options.  Bond prices move inversely with interest rates; a bond put is thus used to hedge against higher
rates. The call price derived from the "Black 76" model thus actually applies to put swaptions while the put price applies
to call swaptions.

A put swaption is better known as a "right-to-pay-fixed" or payer swaption.  Having the right to pay fixed at a predetermined
rate (the strike price) is beneficial if rates rise.  A call swaption is better known as a "right-to-receive-fxed" or receiver 
swaption.  It benefits when rates fall.
"""

"""
ANNUITIZING MODEL PRIZES:
The call price that the option model generates for the put swaption represents 63.49 semiannual basis points for two years
(because the underlying rates were semiannual bond rates).
The up-front price (present value) of the put swaption would be 63.49118 basis points annuitized for the term of the swap.
This represents 31.745 (63.49/2) per period over four periods.  
This price must be discounted by thr two year forward swap rate five years forward (9.6416 or 4.8208 per period)

"""
#{'put': 0.54584416243351719, 'call': 0.63489682074640741}

price = blackSeventySix(SP,EP,r,v,t)
period = 2 * 2 # 
cashflow = price['call']/2.0  
spot = forwardRateCalculator/2.0


def anuitizedModelPricePutSwaption(cashflow,period, spot):
    sum=0.0
    for x in range(1,period+1):
        sum = sum + (1/((1+spot)**(x))) * cashflow
    return sum

print 
#print anuitizedModelPricePutSwaption(cashflow,period, spot)    
print
value_put_swaption = anuitizedModelPricePutSwaption(cashflow,period, spot)/100 * 100000000


print(str(locale.currency(value_put_swaption,grouping=True)) + " : This up-front value of 1.1304 is equivalent to $1,130,400 on a $100 million notional principal amount")


price = blackSeventySix(SP,EP,r,v,t)
period = 2 * 2 # 
cashflow = price['put']/2.0  
spot = forwardRateCalculator/2.0


def anuitizedModelPriceCallSwaption(cashflow,period, spot):
    sum=0.0
    for x in range(1,period+1):
        sum = sum + (1/((1+spot)**(x))) * cashflow
    return sum

print()   
#print anuitizedModelPriceCallSwaption(cashflow,period, spot)   
value_call_swaption = anuitizedModelPriceCallSwaption(cashflow,period, spot)/100 * 100000000
print(str(locale.currency(value_call_swaption,grouping=True))  + " : This up-front value of 0.9718 is equivalent to $971,809.80 on a $100 million notional principal amount")


"""
CHECKING THE VALIDILITY OF THE MODEL:
The validity of the model can be checked by applying the put-call parity theorem.  The put-call parity theorem specifies that:

Price of Call - Price of Put = F - X * e ** (-r * T)    

where

F = value of underlying security at expiration (present value of forward rate at expiration)

X = present value of strike at expiration

r = interest rate and

t = time to expiration.

Sum of t=i to T (Forward Rate - Strike)/(1 - rt)**t

where

r = discount rate for time period t
T = term of the swap
i = first exchange date of the coupons.

For semiannual periods, this is equivalent to:

sum of t = i to T (Forward Rate/2.0 - Strike/2.0)/(1 - rt/2.0)**t

where 
F = 9.6416 #forward rate 
S =  9.50  #strike rate =
cashflow =  9.6416/2.0 - 9.50/2.0 #F/2 - S/2 
period = 4
forwardStartDate = 5
 
def anuitizedModelSpread(cashflow,period, spot,forwardStartDate):
    sum=0.0
    for x in range(1,period+1):
        sum = sum + (1/((1+spot)**(x))) * cashflow
    return sum * discountFactors[forwardStartDate*2 -1]

print
print anuitizedModelSpread(cashflow,period, spot,forwardStartDate)
#0.158587624369

The five-year spot-rate discount factor (DFs) is 0.6290.  The equation aboveis equivalent to:

Spread_Difference = 9.6416/2.0 - 9.50/2.0
print discountFactors[10:] #[0.60024811864734617, 0.57268091862575743, 0.54630785249998259, 0.52107854757298466]
#The above is the discount factor for years 5.5,6.0,6.5and 7.0
#Spread_Difference * (DF5.5 + DF6.0 + DF6.5 + DF7.0)
Spread_Difference * sum(discountFactors[10:])
#0.15861433296410227 or 0.15866

This is the net spread discounted for each of the periods.  Incidentally, 0.1586 is the up-front marked-to-market value for a
forward swap.  A forward swap to pay fixed at a strike at strike of 9.50 would be worth 0.1586 basis points up front.  A forward swap
to receive fixed at 9.50 would be worth -0.1586.  Receiving fixed at 9.50 is below the forward rate 9.4616; therefore a counterparty would require
an up-front payment to enter this swap.)

Thus the present value of a forward swap is

Call(Put Swaption) - Put(Call Swaption)

1.1304 - 0.9718 = 0.1586

Furthermore:

Pay-Fixed Forward Swap = Buy Call (Put Swaption) + Sell Put (Call Swaption)

= 1.1304 - 0.9718 = 0.1586

Received-Fixed Forward Swap

=Sell Call(Put Swaption) + Buy Put(Call Swaption)

= -1.1305 + 0.9718 = -0.1586

Put-call parity implies that the purchase of a long-term straight bond combined with the right to pay fixed (put swaption) is equivalent to the 
purchase of a short-term bond combined with the right to recevie fixed fixed (call swaption). The former is preferable when forward rates
are relatively low and the latter is preferable when forward rates are relatively high.

"""

