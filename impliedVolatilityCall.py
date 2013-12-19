"""
The market implied volatility is of an option is the value of the volatility that is 
implicit in the market price of the option.  If we know the other parameters of an European
call or put we can infer its implied volatility from these parameters.  This code was created
from the pseudocode in the book - A primer for the Mathematics of Financial Engineering and
the code will only work for a call option.  In the near future, we will create a similar one for a put option
and finally combine them in one file.  In order to ensure the accuracy of the code, we compared to the result
generated by MATLAB Financial Instrument Toolbox and the results are close but not the same so we can 
say it is okay from a benckmarking perspective:

MATLAB Code (from Matlab Online Documentation) adapted to the parameters in the book:
AssetPrice = 25;
Settlement = 'Jan-01-2008';
Maturity = 'Dec-31-2008';
Strike = 20;
Rates = 0.05;
OptionPrice = [7.00;];
OptSpec = {'call'};

RateSpec = intenvset('ValuationDate', Settlement, 'StartDates', Settlement,'EndDates', Maturity, 'Rates', Rates, 'Compounding', -1, 'Basis', 1);

StockSpec = stockspec(NaN, AssetPrice);

ImpvVol =  impvbybls(RateSpec, StockSpec, Settlement, Maturity, OptSpec,Strike, OptionPrice)

Result:

ImpvVol = 0.3639

Python Result:
    
round(impliedVolCall(0,25.0,20.0,1.0,0.05,0.00,'call',C=7.0),5)

result:0.36306

The code was also benchmarked against RQuantLib using R and the result converges with the one in the textbook and this
python code:

To use RQuantLib do the following:

>library(RQuantLib) 
> EuropeanOptionImpliedVolatility(type="call", value=7.0, underlying=25.0, strike=20, dividendYield=0.00, 
riskFreeRate=0.05,maturity=1.0, volatility=0.25)

RESULT: 0.363063

Which is the same as the one from the python code above.

    
"""

import math
import scipy
import scipy.stats
import numpy as np

result = 0.0
cdf = 0.0

"""
This is an implementation to calculate CDF using scipy.
This implementation is more straight forward.
"""
def cumm_dens_function_scipy(t):
    return scipy.stats.norm.cdf(t)
    

def blackScholesImpVol(t,S,K,T,a,r,q,Type):
    #t = beginning time
    #S = Spot Price
    #K = Strike
    #T = Maturity
    #a = volatility
    #r = constant interest rate
    #q = continous dividend rate of the underlying asset
    #Type can be call or put - enter as strings e.g. 'call'  - this will only work for call
    call = 0.0
    d1 =0.0
    d2 = 0.0
    S = float(S)
    K = float(K)
    
    d1 = (np.log(S/K) +(r - q + a**2/2)*(T - t))/(a*math.sqrt(T-t))
    d2 = d1 - (a*math.sqrt(T-t))
    
    call = S*math.exp(-q*(T-t))*cumm_dens_function_scipy(d1) - K*math.exp(-r*(T-t))*cumm_dens_function_scipy(d2)

    return call

        
def vegaImpVol(t,S,K,T,a,r,q):
    #t = beginning time
    #S = Spot Price
    #K = Strike
    #T = Maturity
    #a = volatility
    #r = constant interest rate
    #q = continous dividend rate of the underlying asset
    #Type can be call or put - enter as strings e.g. 'call' or 'put'
    d1 = (np.log(S/K) +(r - q + a**2/2)*(T - t))/(a*math.sqrt(T-t))
    return S * math.exp(-q*(T-t)) * math.sqrt(T-t) * (1.0/(math.sqrt(2*math.pi))*math.exp(-d1**2/2.0))
    

#This is the implementation of the Newton-Raphson method

def impliedVolCall(t,S,K,T,r,q,Type,C): #xo is the initial guess #Sample call newton(0.1)
        #t = beginning time
    #S = Spot Price
    #K = Strike
    #T = Maturity
    #a = volatility - is assumed to start at 0.25 here
    #r = constant interest rate
    #q = continous dividend rate of the underlying asset
    #Type can be call or put - enter as strings e.g. 'call' 
    #C = Call Price
    epsilon = 10e-9
    maxIterationCount = 1000000
    xnew = 0.25
    xold=0.0
    xold = xnew-1
    i = 0
    
    while (i < maxIterationCount):
        f_BS_xnew = blackScholesImpVol(t,S,K,T,xnew,r,q,Type)
        vega_BS_xnew = vegaImpVol(t,S,K,T,xnew,r,q)
        xold = xnew

        xnew = xnew - (f_BS_xnew-C)/vega_BS_xnew
        
        if abs(xnew - xold) <= epsilon:
            return xnew
        ++i

#Sample Call
#impliedVolCall(0,25.0,20.0,1.0,0.05,0.00,'call',7.0)
    
