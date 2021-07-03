#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Created on Thu Jun  8 21:03:18 2017
Originally Created: Dec 19, 2013
Revised: June 8, 2017

@author: oluwaseyiawoga
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


"""
This is that implements the Black Scholes Model
It is used as a helper function here
"""

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


"""
Another Helper Function to
calculate the vega of an option.
"""
        
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
    

"""
This is the implementation of the Newton-Raphson method.
This is the main subroutine in this program and it
calls the other helper functions to calculate the 
implied volatility of a stock.
"""

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
        
#
"""
Parameters Per Mini Project 1 (WQU):
Sample Usage & Output.
"""
t = 0  #Beginning Time
S = 34.0
K = 34.0
T = 1
r = 0.001
q = 0.00 #Assumes No Dividend Payments
Type = 'call'
C = 2.2740

print()
print("The Implied Volatility is: ")
print("")
print(impliedVolCall(t,S,K,T,r,q,Type,C))


"""

The Implied Volatility is: 

0.166669428006


Implied volatility is one of the deciding factors in the pricing of options. 
Options, which give the buyer the opportunity to buy or sell an asset at a 
specific price during a pre-determined period of time, have higher premiums 
with high levels of implied volatility, and vice versa. Implied volatility 
approximates the future value of an option, and the option's current value 
takes this into consideration. Implied volatility is an important thing for 
investors to pay attention to; if the price of the option rises, but the buyer 
owns a call price on the original, lower price, or strike price, that means he 
or she can pay the lower price and immediately turn the asset around and sell 
it at the higher price.

It is important to remember that implied volatility is all probability. 
It is only an estimate of future prices, rather than an indication of them. 
Even though investors take implied volatility into account when making investment 
decisions, and this dependence inevitably has some impact on the prices themselves, 
there is no guarantee that an option's price will follow the predicted pattern. 
However, when considering an investment, it does help to consider the actions other 
investors are taking in relation to the option, and implied volatility is directly 
correlated with market opinion, which does in turn affect option pricing.



Source: Implied Volatility - IV http://www.investopedia.com/terms/i/iv.asp#ixzz4kPEcV3Sz 

"""
