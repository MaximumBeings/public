"""
TITLE: Pricing a bond given the zero rate curve.

BACKGROUND:  Recall that we discussed the algorithms for generating the zero curve
a while ago.  Having generated the zero  rate curve how can we use it to value a 
bond.  This program illustrates how we can value a bond using a zero rate curve in a 
rather simplistic manner.  Also recall that we developed a bond valuation program a while back
but that program assumed a flat term structure of interest rate which is not often realistic.

SOURCE: A Primer for the Mathematics of Financial Engineering.  This program is essentially
a translation of the Pseudocode in the book to python.

See you next time!!!!
"""

import math
time = [2,8,14,20]   #The bond matures in 20 months so cashflows are due on the 2nd, 8th, 14th and 20th months
disc_factor = []
cashflow = [3,3,3,103]  #Par value is 100 and interest is 6% on a semi-annual basis.


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
    
#Sample call
#bond_price([3,3,3,103])
#result -> 101.88821588120076 which converges to the solution in the book.



    
