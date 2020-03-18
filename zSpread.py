"""
Market or Risky Price = sum(1 to n)((CF_1to_n)/(1+(r+s)/m)^nm))
Author: Oluwaseyi Awoga
IDE: CS50 IDE on Cloud 9/AWS
Topic: zSpread on Risky Bond Versus Benchmark Treasury Bond
Location: Milky-Way Galaxy
"""
from numpy import array
import numpy as np
from scipy.optimize import fsolve

issuePrice = 98
maturity = 2
r = 0.03 #risk-free rate
c = 0.03  #coupon
notional = 100
numberOfTotalPymnts = 8 #(2 years * 4 payments in a year)

def zSpread(spread):
    discountedValue= 0
    s = spread[0]
    timeElapsed = 0
    for x in range(1,numberOfTotalPymnts+1):
        timeElapsed = timeElapsed + 3
        coupon = 3/12 * c * notional
        temp = coupon/(1+(r+s)/4)**(x)
        discountedValue = discountedValue + temp
    temp = notional/(1+(r+s)/4)**(x)
    discountedValue = temp + discountedValue
    return discountedValue

def optimizationfunc(spread):
    a = issuePrice
    b = zSpread(spread)
    return b - a

solutions = fsolve(optimizationfunc,[0.4/100],xtol=1.49012e-08,)
spreadtoUse = solutions[0]
print("The zSpread on a Risky Bond is: ")
print(spreadtoUse)
print()
print("The Yield To Maturity on the Bond: ")
print(spreadtoUse + r)
print()
print("The Market Price of the Bond Using Zero Spread: ")
print(round(zSpread([0.0])))
print()
print("The Market Price of the Bond Using Optimized zSpread: ")
print(round(zSpread([spreadtoUse])))


"""
The zSpread on a Risky Bond is: 
0.010460524917312954

The Yield To Maturity on the Bond: 
0.04046052491731295

The Market Price of the Bond Using Zero Spread: 
100

The Market Price of the Bond Using Optimized zSpread: 
98.0
"""






