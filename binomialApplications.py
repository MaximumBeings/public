"""
Topic:  Applcaitions of Binomial Short Rate Models

Source: Binomial Pricing of Interest Rate Derivatives - Don Chance 1998

Discussion:  We will be using the above article to model different interest rate instruments such as FRAs, Caps,
Floors, Swaptions and Swaps.  Below is the model for FRAs.   Here we take the short rate mmodel as given...but recall that
we modeled short rate models before.  We will continue with the rest of the implementation next time.
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

