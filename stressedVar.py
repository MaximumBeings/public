"""
#TOPIC: Calculating Yield and Stressed VaR. 

#SOURCE: Introduction to Credit Risk Management - TU Delft via Edx

#DISCUSSION: This is just a conversion of the class sample on calculation of Stressed VaR for randomly generated
# loss distribution from R to Python. I am converting some the course codes (in R) and other manual examples
# to Python just for the sake of doing so. Auditing the class to refresh and while away time.  Refer to the class
# lectures for further details.
"""

import math
#Imagine we have a 2-year bond with face value (also known as par value) equal to
#$100, which pays 5% per annum semiannually, that is a coupon of $2.5 every 6 months.
# The market price of the bond (what we pay today to buy the bond) is $98.97.
#What is the yield of the bond?

#The yield is the rate y which solves the following equation:
#2.5exp(-0.5y)+2.5exp(-1y)+2.5exp(-1.5y) + 102.5exp(-2y)-98.97 = 0

import mpmath
from scipy.optimize import fsolve 


##Define function.

def f(y):
    return 2.5*math.exp(-0.5*y)+2.5*math.exp(-1*y)+2.5*math.exp(-1.5*y)+102.5*math.exp(-2*y)-98.97
    
##Use mpmath library to find the root.
print ""
print "mpmath root - yield"
print mpmath.findroot(f,-3, solver='secant')
print ""

##Or use Scipy's fsolve to find the root.
print "Scipy's root - yield"
print fsolve(f, 0.1)[0]

#bond yield spread, that is to say the difference between the yield of a bond and the risk-free rate on the market. 
#Assume the risk-free rate is 3.00%
#Then the bond yield spread = yield minus 3.00%  = 0.0547-0.0300 = 0.0247
#PD is sometimes defined as CS/1-R where PD is the probability of default, CS is the credit spread and R is the recovery rate
#the bond yield spread is a type of CS



#STRESSED VAR
import numpy as np
mu, sigma = 1, 2 # mean and standard deviation
s = np.random.lognormal(mu, sigma, 100)

print ""
print "VaR for all Losses"
print np.percentile(s,95) # calculate the VaR of the loss distribution at 95% confidence interval
print ""
#sort the array 
s2=np.sort(s)

#get the largest 50 items
wl=s2[51:100]  #worst losses (top 50)
print "VaR for Worst Losses"
print np.percentile(wl,95) # calculate the VaR of the worst losses distribution at 95% confidence interval

"""
RESULTS:
mpmath root - yield
0.0547558137341901

Scipy's root - yield
0.0547558137342

VaR for all Losses
59.9874342694

VaR for Worst Losses
77.3936044183

"""
