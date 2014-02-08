"""
Title: Bond Price, Duration and Convexity of a Bond Given the Yield of the Bond.

Definitions:
    Duration - A measure of the sensitivity of the price (the value of principal) of a fixed-income 
    investment to a change in interest rates. Duration is expressed in number of years. Rising interest 
    rates mean falling bond prices, while declining interest rates mean rising bond prices. the duration 
    of a financial asset that consists of fixed cash flows, for example a bond, is the weighted average 
    of the times until those fixed cash flows are received.  The different types of durations include modified
    duration and macaulay duration.
    
    Convexity: A measure of the curvature in the relationship between bond prices and bond yields that demonstrates 
    how the duration of a bond changes as the interest rate changes. Convexity is used as a risk-management tool, 
    and helps to measure and manage the amount of market risk to which a portfolio of bonds is exposed. In finance, 
    bond convexity is a measure of the sensitivity of the duration of a bond to changes in interest rates, the 
    second derivative of the price of the bond with respect to interest rates (duration is the first derivative). 
    In general, the higher the convexity, the more sensitive the bond price is to the change in interest rates. 

    Sources: Wikipedia and Investopedia and A Primer for the Mathematics of Financial Engineering.
    
See you next time!!!!!  Going forward (if time permits) we will try to be language agnostic and also use Java, C++ and 
C to develop our models in addition to Python.  But at the end of the day, it does not matter which language we use,
because they are all just tools....the most important thing is whether you are able to use your models to make informed 
decisions or not.
    
    
"""


import math
time = [2,8,14,20] #The bond matures in 20 months so cashflows are due on the 2nd, 8th, 14th and 20th months
disc_factor = []
cashflow = [3,3,3,103] #Par value is 100 and interest is 6% on a semi-annual basis.
y = 0.065 #6.5% = yield

def disc_factor(time):
    #Using the yield-to-maturity (ytm) of 6.5% from above we calculate our discount factors as documented below.
    #This program returns a vector of discount factors for the different cashflow payments.
    #This is a different way of discounting a bond using the ytm instead of the zero-rate which we discussed last time.
    #We will repeat this code using a zero-rate curve in the future.
    disc_factor = []
    for x in range(len(time)):
        disc_factor.append(math.exp(-1* time[x]/12.0*y))
    return disc_factor

disc_factor2 = disc_factor(time)
    
def bond_price(cashflow):
    ### The bond price is calculated using the discount factors and the cashflow payments vectors documented above.
    bond_price2 = 0.0
    for x in range(len(cashflow)):
        bond_price2 += (cashflow[x]*disc_factor2[x])
    return bond_price2
    
def duration(cashflow):
    ### The bond duration is calculated using the discount factors and the cashflow payments and time vector from above.
    duration = 0.0
    for x in range(len(cashflow)):
        duration += cashflow[x]*disc_factor2[x]*(time[x]/12.0)
    return duration/bond_price(cashflow)
    
def convexity(cashflow):
    ### The bond convexity is calculated using the discount factors and the cashflow payments and time vector from above.
    convexity = 0.0
    for x in range(len(cashflow)):
        convexity += cashflow[x]*disc_factor2[x]*(time[x]/12.0)*(time[x]/12.0)
    return convexity/bond_price(cashflow)
    
#Sample call
#bond_price([3,3,3,103])
#result -> 101.04619291323598 which converges to the solution in the book.
#duration([3,3,3,103])
#result ->  1.5804215018374825 which converges to the solution in the book.
#convexity([3,3,3,103])
#result -> 2.5916858802726863  which converges to the solution in the book.



