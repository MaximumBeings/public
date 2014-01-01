"""
TITLE:  BOOTSTRAPPING ZERO RATE CURVES.

DEFINITION: The Zero Rate r(0,t) between time 0 and time t is the
rate of return of a cash deposit made at time 0 and maturing at time t.
The zero-coupon yield or spot-rate curve is the term structure of discount 
rate of zero-coupon bonds.  A zero curve consists of the yield to maturity
for a portfolio of theoretical zero-coupon bonds that are derived from the 
input bonds portfolio.

STATEMENT OF PROBLEM: The coupon rate or treasury rates are only available for
certain maturity so we need to bootstrap for dates for which there are no available rate.

Consider the example below - from A Primer for the Mathematics of Financial Engineering -
The Prices and coupon rates for four semiannual coupon bonds with face value of 100 are as follows:

Maturity    Coupon Rate     Price
6 Months    0               99
1 Year      4               102
2 Years     4               103.5
5 Years     4               109

As you can see above, we only have information for 6 months, 1 year, 2 years and 5 years.  However, the bond
portfolio consists of semi-annual coupon paying bonds so we need information for 1.5 year's time, 2.5 year's time, 3 year's time,
4 year's time,4.5 year's in order to determine the price of a 3 year semi-annual bond etc.  So to achieve this objective, we have to bootstrap
the zero rate using a mixture of interpolation and bootstrapping using Newton-Raphson.

The key assumption made in the book is that the cashflow are continously compounded and the formula for bootstrapping the zero rate is a little 
bit different if the bond pays no coupon versus if it pays coupon.  In order to follow along you have to get a copy of the book or borrow it from 
the library or your friend. (see page 153)

 ***This is a really rough prototype and will only work for the question in the book.  However, if you know python you can edit the code to work for
 other bond portfilio.  We will update it to work for different length of maturity such as 10 years etc. i.e. make it more dynamic. Making it dynamic
 will require using python to calculate the first derivatives used in the Newton-Raphon module instead of using Wolfram Alpha
"""

#To bootstrap the zero rate for the 6 months zero-coupon paying bond we use the formula below:
import math

#To bootstrap the zero rate for the 6 months zero-coupon paying bond we use the formula below:
r06 =  (12.0/6)*math.log(100.0/99)

print "r06 is " + str(r06)

#To calculate the root of the original function - this function can be changed to a new one.


def func_calculator1(x):  #Price Function for Year 1
    return 102.0 - 2 *math.exp(-0.5*0.0201007) - 102*math.exp(-x)
    
#To calculate the root of the first derivative of the function.

def func_prime_calculator1(x):  #Derivative of Price Function for Year 1
    return 102.0*math.exp(-x)
    
    
def func_calculator2(x):  #Price Function for Year 2
    return 103.5 - 2.0*math.exp(-0.5*0.0201007) - 2.0*math.exp(-1*0.0196026) - 2.0*math.exp((-1.5*(0.0196026+x))/2.0) - 102*math.exp(-2.0*x)
    
#To calculate the root of the first derivative of the function.

def func_prime_calculator2(x):  #Derivative of Price Function for Year 2
    return 204.0*math.exp(-2.0*x) + 1.47811*math.exp(-0.75*x)
    #return 5.17955*math.exp(-2.66667*x) + 3.36814*math.exp(-1.75*x) + 1.91412*math.exp(-x) + 0.796093*math.exp(-0.41667*x) +510*math.exp(-5*x) + 7.37757*math.exp(-3.75*x)
    
def func_calculator5(x):  #Price Function for Year 5
    return 109.0 - 2.0*math.exp(-0.5*0.0201007) - 2.0*math.exp(-1*0.0196026) - 2.0*math.exp(-1.5*0.02077345) - 2*math.exp(-2.0*0.0219443) - 2.0*math.exp((-2.5*(x+(5*0.0219443))/6.0)) - \
    2.0*math.exp((-3.0*(x+(2*0.0219443))/3.0)) - 2.0*math.exp((-3.5*(x+(0.0219443))/2.0)) - 2.0*math.exp((-4.0*(2*x+(0.0219443))/3.0)) - 2.0*math.exp((-4.5*(5*x+(0.0219443))/6.0)) - 102*math.exp(-5*x)

#To calculate the root of the first derivative of the function.

def func_prime_calculator5(x):  #Derivative of Price Function for Year 5
    return 5.17955*math.exp(-2.66667*x) + 3.36814*math.exp(-1.75*x) + 1.91412*math.exp(-x) + 0.796093*math.exp(-0.41667*x) +510*math.exp(-5*x) + 7.37757*math.exp(-3.75*x)
    


#This is the implementation of the Newton-Raphson method

def newton1(x): #Newton call for year 1
    epsilon = 10e-9
    maxIterationCount = 1000000
    x0 = x
    x1 = 0.0
    i = 0
    try:
        while (i < maxIterationCount):
            fValue = func_calculator1(x0)
            fDerivative = func_prime_calculator1(x0)

            x1 = x0 - fValue/fDerivative
        
            if abs(x1 - x0) <= epsilon:
                return x1
        
            x0 = x1
            ++i
    except (OverflowError,RuntimeError, TypeError, NameError):
        print""
        print "No Solution Was Found!!!."
        

def newton2(x): #Newton call for year 2
    epsilon = 10e-9
    maxIterationCount = 1000000
    x0 = x
    x1 = 0.0
    i = 0
    try:
        while (i < maxIterationCount):
            fValue = func_calculator2(x0)
            fDerivative = func_prime_calculator2(x0)

            x1 = x0 - fValue/fDerivative
        
            if abs(x1 - x0) <= epsilon:
                return x1
        
            x0 = x1
            ++i
    except (OverflowError,RuntimeError, TypeError, NameError):
        print""
        print "No Solution Was Found!!!."
        
def newton5(x): #Newton call for year 5
    epsilon = 10e-9
    maxIterationCount = 1000000
    x0 = x
    x1 = 0.0
    i = 0
    try:
        while (i < maxIterationCount):
            fValue = func_calculator5(x0)
            fDerivative = func_prime_calculator5(x0)

            x1 = x0 - fValue/fDerivative
        
            if abs(x1 - x0) <= epsilon:
                return x1
        
            x0 = x1
            ++i
    except (OverflowError,RuntimeError, TypeError, NameError):
        print""
        print "No Solution Was Found!!!."
        
r6 = 0.020100
r12 = newton1(0.05)
r18 = (0.0196026 +0.0219443)/2.0
r24= newton2(0.05)  # Value is 0.021944274982594374
r30= (0.020801859402415773 + 5*0.0219443)/6.0
r36= (0.020801859402415773 +2*0.0219443)/3.0
r42= (0.020801859402415773 + 0.0219443)/2.0
r48= (2*0.020801859402415773 + 0.0219443)/3.0
r54= (5*0.020801859402415773 + 0.0219443)/6.0
r60= newton5(0.05)  ### Value is 0.020801859402415773

data = {}
data.update({"r06": r06})
data.update({"r12": r12})
data.update({"r18": r18})
data.update({"r24": r24})
data.update({"r30": r30})
data.update({"r36": r36})
data.update({"r42": r42})
data.update({"r48": r48})
data.update({"r54": r54})
data.update({"r60": r60})

import pandas as pd
print ""
df = pd.Series(data)
df.plot()


#Sample Output
"""
r06    0.020101         - Six Months
r12    0.019603         - Year 1
r18    0.020773         - Year 1.5
r24    0.021944         - Year 2
r30    0.021754         - Year 2.5
r36    0.021563         - Year 3
r42    0.021373         - Year 3.5
r48    0.021183         - Year 4
r54    0.020992         - Year 4.5
r60    0.020802         - Year 5

"""


