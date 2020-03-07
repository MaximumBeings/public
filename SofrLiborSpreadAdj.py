"""
Author: Oluwaseyi Awoga
IDE: CS50 IDE on Cloud 9/AWS
Topic: Optimization of SOFR Spread Adjustment Calculation
Location: Milky-Way Galaxy
"""

from datetime import date
from numpy import array
import numpy as np
from scipy.optimize import fsolve



contractDate = date(2017, 9, 30)

interestPaymentDates = [date(2017, 12, 31), date(2018, 3, 31),date(2018, 6, 30),\
                       date(2018, 9, 30), date(2018, 12, 31), date(2019, 3, 31),\
                       date(2019, 6, 30), date(2019, 12, 31)]

liborRates = [0.50/100, 0.75/100, 1.00/100, 1.25/100, 1.50/100, 1.75/100, 2.00/100, 2.25/100]

sofrRates = [0.4/100, 0.6/100, 0.8/100, 1.00/100,1.20/100,1.4/100,1.6/100,1.8/100]

notional = 1000000000.00

def liborInterests():
    totalInterest = 0.0
    for x in range(len(interestPaymentDates)):
        if x == 0:
            period = (interestPaymentDates[x] - contractDate).days
            quarterlyInterest = (period/365 * liborRates[x])* notional
            totalInterest = totalInterest + quarterlyInterest

        elif x != 0:
            period = (interestPaymentDates[x] - interestPaymentDates[x-1]).days
            quarterlyInterest = (period/365 * liborRates[x])* notional
            totalInterest = totalInterest + quarterlyInterest

    return totalInterest


def sofrInterests(spread):
    totalInterest = 0.0
    s = spread[0]
    for x in range(len(interestPaymentDates)):
        if x == 0:
            period = (interestPaymentDates[x] - contractDate).days
            quarterlyInterest = (period/365 * (sofrRates[x]+s))* notional
            totalInterest = totalInterest + quarterlyInterest

        elif x != 0:
            period = (interestPaymentDates[x] - interestPaymentDates[x-1]).days
            quarterlyInterest = (period/365 * (sofrRates[x]+s))* notional
            totalInterest = totalInterest + quarterlyInterest

    return totalInterest


def optimizationfunc(spread):

    a = liborInterests()
    b = sofrInterests(spread)

    return a - b


solutions = fsolve(optimizationfunc,[0.4/100],xtol=1.49012e-08,)
spreadtoUse = solutions[0]

print()
print("Response to Federal Reserve's Call for Consultation on SOFR Spread Adjsutment")
print()

print("Total LIBOR Interest: ")
print(round(liborInterests(),2))
print()

print("Total SOFR Interest Before Spread: ")
print(round(sofrInterests(array([0.0])),2))
print()

print("Spread Calculated Using Optimization; " + str(spreadtoUse))
print()

print("Total SOFR Interest plus Spread: ")
print(round(sofrInterests(array([spreadtoUse])),2))
print()

print("Difference between LIBOR & SOFR Before Spread: ")
print(round(liborInterests() - sofrInterests(array([0.0])),2))
print()

print("Difference between LIBOR & SOFR With Spread: ")
print(round(liborInterests() - sofrInterests(array([spreadtoUse])),2))
print()

"""
Response to Federal Reserve's Call for Consultation on SOFR Spread Adjsutment                                                                           
                                                                            
Total LIBOR Interest:                                                       
33178082.19                                                                 
                                                                            
Total SOFR Interest Before Spread:                                          
26542465.75                                                                 
                                                                            
Spread Calculated Using Optimization; 0.0029464720194647166                 
                                                                            
Total SOFR Interest plus Spread:                                            
33178082.19                                                                 
                                                                            
Difference between LIBOR & SOFR Before Spread:                              
6635616.44                                                                  
                                                                            
Difference between LIBOR & SOFR With Spread:                                
0.0           
"""









