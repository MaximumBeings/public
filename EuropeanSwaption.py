"""
Topic: A Simple Method For Pricing Interest Rate Swaptions (40% Done)

Source: FA Journal By the CFA Institute 1991 By David R. Smith

Discussion: 40% Done. The model below pretty much shows how to bootstrap spot rate from YTM.   We have done this 
before several times but consider it a refresher and a slightly different approach.  We used numerical methods
to bootstrap the semi-annual spot rates but we could have calculated them analytically.  May be we will do it 
analytically soon.  Anyways, what we have done so far will feed into our model to price a European Swaption.  We
will continue with the implementation soon. The output from this model are the spot rates and discount rates.
See you next time!!!

"""



from __future__ import division
from math import exp, sqrt
from scipy.optimize import fsolve
import math
import sys
import copy

"""
Year        Swap_Rate_YTM        Coupon
0.5         8.8700               0.04435
1           9.0400               0.04520
1.5         9.1550               0.04578
2           9.2700               0.04635
2.5         9.3150               0.04658
3           9.3600               0.04680
3.5         9.3850               0.04693
4           9.4100               0.04705
4.5         9.4350               0.04718
5           9.4600               0.04730
5.5         9.4700               0.04735
6           9.4800               0.04740
6.5         9.4900               0.04745
7           9.5000               0.04750
              
"""
def boostrapHelper(gUESS,tIME,yTM,sPOT):
    collector = 0.0
    rate2=[]
    rate=[]
    for x in range(len(tIME)):            
        if x == len(tIME) - 1:
            y = yTM[0]
            g = gUESS[0]
            t = tIME[x]
            collector = ((100 + y/2.0)/(1+g/2.0)**(t*2))
            rate.append(collector)
        else:
            y = yTM[0]
            s = sPOT[x]
            t = tIME[x]
            collector = ((y/2.0)/(1+s/2.0)**(t*2))
            rate.append(collector)
        collector = 0.0
        rate2=rate[:]
            
    return (100- sum(rate2))
    
tIME = [0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7]
yTM = [8.8700, 9.0400,9.155,9.2700,9.3150,9.3600,9.3850,9.4100,9.4350,9.4600,9.4700,9.4800,9.4900,9.5000]
gUESS = [0.12]
#yTM = [9.155]
#
#sPOT=[]
#sPOT.append(yTM1[0]/100)
#sPOT = [0.08869999999999999,0.090438452331122077]

#
#data = ([0.5,1,1.5], [9.155])
#fsolve(boostrapHelper,gUESS,args=data)[0]

def bootStrapper(tIME, yTM, gUESS):
    sPOT=[]
    
    for x in range(len(tIME)):
        if x == 0:
            sPOT.append(yTM[0]/100)
        else:
            tIME2 = tIME[:x+1]
            yTM2 = [yTM[x]]
            data = (tIME2,yTM2,sPOT)

            sPOT.append(fsolve(boostrapHelper,gUESS,args=data)[0])

    return sPOT
        
"""
Calculate Discount Rate from Zero Rates
"""

zeroRates = bootStrapper(tIME, yTM, gUESS)



def discountFactorCalculator(zeroRates,tIME):
    discountRates = []
    for x in range(len(zeroRates)):
        discountRates.append(1/((1+zeroRates[x]/2.0)**(tIME[x]*2)))
    return discountRates
        
discountFactors = discountFactorCalculator(zeroRates,tIME)



import pandas as pd

d = {'Time' : pd.Series(tIME),'YTM' : pd.Series(yTM),'Spot Rates' : pd.Series(zeroRates),'Disc_Factors' : pd.Series(discountFactors)}

print

df = pd.DataFrame(d,columns=['Time', 'YTM', 'Spot Rates', 'Disc_Factors'])

print(df.to_string())


"""
OUTPUT


    Time    YTM  Spot Rates  Disc_Factors
    
0    0.5  8.870    0.088700      0.957533
1    1.0  9.040    0.090438      0.915346
2    1.5  9.155    0.091629      0.874250
3    2.0  9.270    0.092843      0.834014
4    2.5  9.315    0.093309      0.796129
5    3.0  9.360    0.093789      0.759595
6    3.5  9.385    0.094051      0.724935
7    4.0  9.410    0.094322      0.691660
8    4.5  9.435    0.094601      0.659718
9    5.0  9.460    0.094887      0.629062
10   5.5  9.470    0.094989      0.600248
11   6.0  9.480    0.095096      0.572681
12   6.5  9.490    0.095208      0.546308
13   7.0  9.500    0.095324      0.521079

"""




