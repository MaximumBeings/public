"""
Title: Bond Price, Duration and Convexity of a Bond Given the Zero Rate Curve

Definitions:
    
Duration - A measure of the sensitivity of the price (the value of principal) of a fixed-income
investment to a change in interest rates. Duration is expressed in number of years. Rising interest
rates mean falling bond prices, while declining interest rates mean rising bond prices. the duration
of a financial asset that consists of fixed cash flows, for example a bond, is the weighted average
of the times until those fixed cash flows are received. The different types of durations include modified
duration and macaulay duration.

Convexity: A measure of the curvature in the relationship between bond prices and bond yields that demonstrates
how the duration of a bond changes as the interest rate changes. Convexity is used as a risk-management tool,
and helps to measure and manage the amount of market risk to which a portfolio of bonds is exposed. In finance,
bond convexity is a measure of the sensitivity of the duration of a bond to changes in interest rates, the
second derivative of the price of the bond with respect to interest rates (duration is the first derivative).
In general, the higher the convexity, the more sensitive the bond price is to the change in interest rates.

Sources: Wikipedia and Investopedia and A Primer for the Mathematics of Financial Engineering.

See you next time!!!!! Going forward (if time permits) we will try to be language agnostic and also use Java, C++ and
C to develop our models in addition to Python. But at the end of the day, it does not matter which language we use,
because they are all just tools....the most important thing is whether you are able to use your models to make informed
decisions or not.

NB: Note that we created something similar recently but we used the yield of the bond to generate the discount factors.
In this version we used the zero rate curve to do our calculations.  In the near future, we will examine the relationship
between zero rate, discount curve and forward curve because these topics are germane to understanding the topics we will
address eventually.

Remember that love is a beautiful thing ..... Happy Valentine's Day.
"""

import math
time = [2,8,14,20] #The bond matures in 20 months so cashflows are due on the 2nd, 8th, 14th and 20th months
disc_factor = []
cashflow = [3,3,3,103] #Par value is 100 and interest is 6% on a semi-annual basis.


def zero_rate(t):
    #We are making the assumption that the zero rate is generated using the formula below
    #but in real life it is generated using a combination of bootstrapping and interpolation.
    #We have already discussed this so we will just assume that it is correct.
    return 0.0525 + math.log(1 + 2 * t)/200.00

def disc_factor(time):
    #Using the zero rates calculated above we calculate our discount factors as documented below.
    #This program returns a vector of discount factors for the different cashflow payments
    disc_factor = []
    for x in range(len(time)):
        disc_factor.append(math.exp(-1* time[x]/12.0*zero_rate(time[x]/12.0)))
    return disc_factor

disc_factor2 = disc_factor(time)
    
def bond_price(cashflow):
    ###Finally we use the discount factors and the cashflow payments to calculate the bond price.
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
#result -> 1.5804215018374825 which converges to the solution in the book.
#convexity([3,3,3,103])
#result -> 2.5916858802726863 which converges to the solution in the book.
