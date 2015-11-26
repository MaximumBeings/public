"""
Topic:  Applcaitions of Binomial Short Rate Models

Source: Binomial Pricing of Interest Rate Derivatives - Don Chance 1998

Discussion:  We will be using the above article to model different interest rate instruments such as FRAs, Caps,
Floors, Swaptions and Swaps.  Below is the model for FRAs.   Here we take the short rate mmodel as given...but 
recall that we modeled short rate models before.  We will continue with the rest of the implementation next time.
Will be featured in an upcoming article.  One Love!!!

PLAN:
FRAs -  Done
Interest Caps and Floors  - Pending
Interest Rate Swaps  - Pending
Interest Rate Swaption - Pending
"""

from scipy.optimize import fsolve

"""

#############################################################
#
#Node 0    Node 1      Node 2      Node 3       Node 4       
#
#                                                            
#                                               16.72%
#                                  15.15%                 
#                       13.61%                  13.32%
#            12.06%                11.80%                     
#10.50%                 10.30%                  10.02%
#             8.80%                 8.54%                 
#                        7.09%                   6.82%
#                                   5.38%                 
#                                                3.71%
#                                                            
#
#############################################################

"""

intRateTree = [[0.105], [0.1206,0.0880], [0.1361, 0.1030, 0.0709], [0.1515,0.1180,0.0854,0.0538], [0.1672, 0.1332, 0.1002, 0.0682, 0.0371]]

"""
                 0                   1                   2                   3                   4
------------------|-------------------|-------------------|-------------------|-------------------
                                                                                0.1672000000000000
                                                            0.1515000000000000  0.1332000000000000
                                        0.1361000000000000  0.1180000000000000  0.1002000000000000
                    0.1206000000000000  0.1030000000000000  0.0854000000000000  0.0682000000000000
0.1050000000000000  0.0880000000000000  0.0709000000000000  0.0538000000000000  0.0371000000000000

"""


def forwardRateAgreements(gUESS,tIME, tREE):
    result = []
    for x in range(tIME+1):
        tracker = 1
        if x == 0 or x == len(tREE[tIME]) - 1 :
            
            for y in range(tIME):
                tracker = tracker * 0.5
            result.append(tracker * (tREE[tIME][x] - gUESS)/(1 + tREE[tIME][x]))
        else:
            tracker = 1
            for y in range(tIME):
                tracker = tracker * 0.5
            tracker = tracker * 2
            result.append(tracker * (tREE[tIME][x] - gUESS)/(1 + tREE[tIME][x]))
    return sum(result)
    
FRAs = []
for x in range(5):
    
    data = (x,intRateTree)
    mo = fsolve(forwardRateAgreements,0.1,args=data)
    FRAs.append(mo[0])
    
    
import pandas as pd

tIME = [0,1,2,3,4]

d = {'Time' : pd.Series(tIME),'FRAs' : pd.Series(FRAs)}

print

df = pd.DataFrame(d,columns=['Time', 'FRAs'])

print(df.to_string(index=False))

"""
 Time      FRAs
    0  0.105000
    1  0.104059
    2  0.102768
    3  0.101134
    4  0.099497

"""

"""
Below is a crude prototype I created for calculating caps and floors
will be converted to a function by this weekend
"""

"""
Interest Rate Caps and Floors:
    An interest rate cap is a series of independent call options on an
    interest rate while a floor is aseries of independent put options on
    interest rate. For example, a three-period cap with a strike rate of
    10% contains a call option on the rate with a strike rate of 10% 
    expiring at time 1, another call option on the rate with a strike rate 
    of 10% expiring at time 2, and a third call option on the rate with a 
    strike rate of 10% expiring at time 3.
    
    The value of a cap or floor is the sum of the values of the component options, 
    called caplets or floorlets.
    
    EXAMPLE:
    Consider a four-period cap on the one-period rate struck at 9%. The cap consists
    of four component caplets, one expiring at time 1, one at time 2, one at time 3, and
    one at time 4.  On each caplet expiration date, the cap pays off the one-period rate
    minus the strike rate if the former is higher and zero if the latter is higher.
    
    PROCEDURE
    (a) First value the four-period caplet.  The formula for the payoff of a caplet is
    Max(0, interest rate - exercise rate)/(1 + interest rate)
    
    The discount in the denominator is because  the payoff is made one period later.  In
    other words, if "interesr rate - exercise rate" is positive, the payoffs is made one
    period later. Hence, we discount by the current one-period rate.
    
    (b) Declare variables for the cap.
    maturity = 4
    strike = 0.09
    intRateTree = [[0.105], [0.1206,0.0880], [0.1361, 0.1030, 0.0709], [0.1515,0.1180,0.0854,0.0538], [0.1672, 0.1332, 0.1002, 0.0682, 0.0371]]
    
    payOffTree = intRateTree[maturity]
    payOffListCollector = []
    for x in range(len(payOffTree)):
        payOffListCollector.append(max(0, (payOffTree[x] - strike)/(1 + payOffTree[x]))
    print payOffListCollector
        
"""
maturity = 4
strike = 0.09

payOffTree = intRateTree[maturity]
payOffListCollector = []
for x in range(len(payOffTree)):
    payOffListCollector.append(max(0, (payOffTree[x] - strike)/(1 + payOffTree[x])))
print payOffListCollector 

interMediateTree = intRateTree[:maturity]
interMediateTree.append(payOffListCollector)
interMediateTree

newMaturity = maturity - 1
time3Tree = []
#length = len(newMaturity)
time3 = interMediateTree[3]
for x in   range(len(time3)):
    a = payOffListCollector[x]*0.5 
    b = payOffListCollector[x+1]*0.5
    c = (a+b)/(1+time3[x])
    time3Tree.append(c)
print time3Tree

payOffListCollector = time3Tree

time2Tree = []
time2 = interMediateTree[2]

for x in   range(len(time2)):
    a = payOffListCollector[x]*0.5 
    b = payOffListCollector[x+1]*0.5
    c = (a+b)/(1+time2[x])
    time2Tree.append(c)
print time2Tree

payOffListCollector = time2Tree




time1Tree = []
time1 = interMediateTree[1]

for x in   range(len(time1)):
    a = payOffListCollector[x]*0.5 
    b = payOffListCollector[x+1]*0.5
    c = (a+b)/(1+time1[x])
    time1Tree.append(c)
print time1Tree

payOffListCollector = time1Tree




time0Tree = []
time0 = interMediateTree[0]

for x in   range(len(time0)):
    a = payOffListCollector[x]*0.5 
    b = payOffListCollector[x+1]*0.5
    c = (a+b)/(1+time0[x])
    time0Tree.append(c)
print time0Tree

payOffListCollector = time0Tree


"""
Final Answer = payOffListCollector[0]
#0.011051923090166128 same as in the journal
"""

"""
Automation of the interest rate cap completed.  This is the final function...all the helper 
functions not included.  Will be published in an upcoming article
"""

def finalPrice(maturity, strike, intRateTree):
    finalOutPut = []
    for g in range(maturity,0,-1):
        finalOutPut.append(semiFinal(g, strike, intRateTree)[0])
    return finalOutPut

prices = finalPrice(maturity, strike, intRateTree)

prices[::-1]
print
print
for x in range(0,4):
    print "Time " + str(x+1) + ":   " + str(prices[x])
    

capPrices = sum(prices)
print
print "The Price of a Cap Expiring in Four Years is : " + str(round(capPrices,5))

"""
Time 1:   0.0110519230902
Time 2:   0.0116238731623
Time 3:   0.0130228065338
Time 4:   0.0123560180672

The Price of a Cap Expiring in Four Years is : 0.04805

"""

