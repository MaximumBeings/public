"""
Topic: A Simple Method For Pricing Interest Rate Swaptions (40% Done)

Source: FA Journal By the CFA Institute 1991 By David R. Smith

Discussion: 40% Done. The model below pretty much shows how to bootstrap spot rate from YTM.   We have done this 
before several times but consider it a refresher and a slightly different approach.  We used numerical methods
to bootstrap the semi-annual spot rates but we could have calculated them analytically.  May be we will do it 
analytically soon.  Anyways, what we have done so far will feed into our model to price a European Swaption.  We
will continue with the implementation soon. The output from this model are the spot rates and discount rates.
See you next time!!!

Addendum: The model is done but I did not release the codes just shells where applicable.  Now we are going to 
test the validity of the model using put-call parity as done in the Journal.  See you next time!!

"""



from __future__ import division
from math import exp, sqrt
from scipy.optimize import fsolve
import math
import sys
import copy

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



import pandas as pd

d = {'Time' : pd.Series(tIME),'YTM' : pd.Series(yTM),'Spot Rates' : pd.Series(zeroRates),'Disc_Factors' : pd.Series(discountFactors)}

print

df = pd.DataFrame(d,columns=['Time', 'YTM', 'Spot Rates', 'Disc_Factors'])

print(df.to_string())


"""
OUTPUT


    Time    YTM  Spot Rates  Disc_Factors
    
0    0.5  8.870    0.088700      0.957533
1    1.0  9.040    0.090438      0.915346
2    1.5  9.155    0.091629      0.874250
3    2.0  9.270    0.092843      0.834014
4    2.5  9.315    0.093309      0.796129
5    3.0  9.360    0.093789      0.759595
6    3.5  9.385    0.094051      0.724935
7    4.0  9.410    0.094322      0.691660
8    4.5  9.435    0.094601      0.659718
9    5.0  9.460    0.094887      0.629062
10   5.5  9.470    0.094989      0.600248
11   6.0  9.480    0.095096      0.572681
12   6.5  9.490    0.095208      0.546308
13   7.0  9.500    0.095324      0.521079

"""


"""
OUTPUT - edited to include forward rates, future value and annual spot rates - forward rates calculated using two 
methods - codes not released for these new features. Now 65% completed...to be continued. Done over the
weekend...but forgot to update on github.

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
    return result

print

print blackSeventySix(SP,EP,r,v,t)

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



print 
#print anuitizedModelPricePutSwaption(cashflow,period, spot)    
print
value_put_swaption = anuitizedModelPricePutSwaption(cashflow,period, spot)/100 * 100000000
print str(locale.currency(value_put_swaption,grouping=True)) + " : This up-front value of 1.1304 is equivalent to $1,130,400 on a $100 million notional principal amount"

print
value_call_swaption = anuitizedModelPriceCallSwaption(cashflow,period, spot)/100 * 100000000
print str(locale.currency(value_call_swaption,grouping=True))  + " : This up-front value of 0.9718 is equivalent to $971,809.80 on a $100 million notional principal amount"

"""
$1,130,357.33 : This up-front value of 1.1304 is equivalent to $1,130,400 on a $100 million notional principal amount

$971,809.80 : This up-front value of 0.9718 is equivalent to $971,809.80 on a $100 million notional principal amount

"""
"""
CHECKING THE VALIDILITY OF THE MODEL:
The validity of the model can be checked by applying the put-call parity theorem.  The put-call parity theorem specifies that:

Price of Call - Price of Put = F - X * e ** (-r * T)    

where

F = value of underlying security at expiration (present value of forward rate at expiration)

X = present value of strike at expiration

r = interest rate and

t = time to expiration.

To be continued.........
    
"""


