"""
Topic: BDT Prototype in Python

Source: A One-Factor Model of Interest Rates and Its Application To Treasury Bond Options.

Discussion:  Need to verify my final output wit other sources.  I am sure the output I generated is correct but it is not the same as
as the one in the article perhaps due to the interpolation methodology and round. I used Scipy...having said that I will double
check with other journals and articles and revisit the design.  I already did this before using R but decided to do same again
using the original essay by BDT now I have to revisit again to make sure this is right before I automate it.
I got exactly the same on the first node (time period 1) and I did the verification (see below) and my rates reverts back to
the volatility.  Anyways, ran out of time...See you next time.  I will get to the bottom of this :)
"""






from __future__ import division
import sys
import math 
from scipy.optimize import fsolve


        
"""
Maturity            Yield(%)       Yield_Volatility
1                   10             20
2                   11             19
3                   12             18
4                   12.5           17
5                   13             16

"""
        
r = [0.1,0.11,0.12,0.125,0.13]
vol = [0.20,0.19,0.18,0.17,0.16]
m = 0.03  #guess

a1 = 100/(1+0.11)**2  #Calculate Price from year 2
a2 = 100/(1+0.12)**3
a3 = 100/(1+0.125)**4
a4 = 100/(1+0.13)**5


def bdtOne(guess):
    ru = guess * math.exp(2 * vol[1])
    rd = guess 
    N1 = (100)/(1+ru)
    N2 = (100)/(1+rd)
    return (0.5*((N1/(1+r[0])) + (N2/(1+r[0])))-a1)
    
g = fsolve(bdtOne,m)[0]

ru = g * math.exp(2 * vol[1])
rd = g





def bdtTwo(guess):
    ruu = guess * math.exp(4 * vol[2])
    rud = guess * math.exp(2 * vol[2])
    rdd = guess
    N1 = (100)/(1+ruu)
    N2 = (100)/(1+rud)
    N3 = (100)/(1+rdd)
    ans1 = (0.5*N1 + 0.5*N2)/(1+ru)
    ans2 = (0.5*N2 + 0.5*N3)/(1+rd)
    
    return ((0.5*ans1 + 0.5*ans2)/(1+r[0])-a2)

g = fsolve(bdtTwo,m,xtol=1.49012e-08)[0]

ruu = g * math.exp(4 * vol[2])
rud = g * math.exp(2 * vol[2])
rdd = g



# Verification
vol2 = math.log(ruu/rud)*0.5
math.log(rud/rdd)*0.5
vol2 = 0.18
math.log(ruu/rud)*0.5
math.log(rud/rdd)*0.5
#0.17999999999999994


def bdtThree(guess):
    ruuu = guess * math.exp(6 * vol[3])
    ruud = guess * math.exp(4 * vol[3])
    rdud = guess * math.exp(2 * vol[3])
    rddd = guess
  
    N1 = 100/(1+ruuu) 
    N2 = 100/(1+ruud)
    N3 = 100/(1+rdud)
    N4 = 100/(1+rddd)
    
    ans1 = ((0.5*N1 + 0.5*N2))/(1 + ruu)
    ans2 = ((0.5*N2 + 0.5*N3))/(1 + rud)
    ans3 = ((0.5*N3 + 0.5*N4))/(1 + rdd)
    
    fans1 = ((0.5*ans1 + 0.5*ans2))/(1 + ru)
    fans2 = ((0.5*ans2 + 0.5*ans3))/(1 + rd)
    
    return((0.5*fans1 + 0.5*fans2)/(1+r[0]) - a3)

g = fsolve(bdtThree,m,xtol=1.49012e-08)[0]


ruuu = g * math.exp(6 * vol[3])
ruud = g * math.exp(4 * vol[3])
rdud = g * math.exp(2 * vol[3])
rddd = g


vol2 = math.log(ruuu/ruud)*0.5
math.log(ruud/ruud)*0.5
vol2 = 0.17
math.log(ruuu/ruud)*0.5
math.log(rdud/rddd)*0.5
#0.16999999999999994

def bdtFour(guess):
    ruuuu = guess * math.exp(8 * vol[4])
    ruuud = guess * math.exp(6 * vol[4])
    rudud = guess * math.exp(4 * vol[4])
    ruddd = guess * math.exp(2 * vol[4])
    rdddd = guess 
  
    N1 = 100/(1+ruuuu) 
    N2 = 100/(1+ruuud)
    N3 = 100/(1+rudud)
    N4 = 100/(1+ruddd)
    N5 = 100/(1+rdddd)
    
    ans1 = ((0.5*N1 + 0.5*N2))/(1 + ruuu)
    ans2 = ((0.5*N2 + 0.5*N3))/(1 + ruud)
    ans3 = ((0.5*N3 + 0.5*N4))/(1 + rdud)
    ans4 = ((0.5*N4 + 0.5*N5))/(1 + rddd)
    
    fans1 = ((0.5*ans1 + 0.5*ans2))/(1 + ruu)
    fans2 = ((0.5*ans2 + 0.5*ans3))/(1 + rud)
    fans3 = ((0.5*ans3 + 0.5*ans4))/(1 + rdd)
    
    xans1 = ((0.5*fans1 + 0.5*fans2))/(1 + ru)
    xans2 = ((0.5*fans2 + 0.5*fans3))/(1 + rd)
    
    return((0.5*xans1 + 0.5*xans2)/(1+r[0]) - a4)


g = fsolve(bdtFour,m,xtol=1.49012e-08)[0]

ruuuu = g * math.exp(8 * vol[4])
ruuud = g * math.exp(6 * vol[4])
rudud = g * math.exp(4 * vol[4])
ruddd = g * math.exp(2 * vol[4])
rdddd = g 

vol2 = math.log(ruuuu/ruuud)*0.5
math.log(rudud/ruddd)*0.5
vol2 = 0.16
math.log(ruuuu/ruuud)*0.5
math.log(ruuud/rudud)*0.5
#0.16000000000000003


finalRate = [[0.1],[ru,rd],[ruu,rud,rdd],[ruuu,ruud,rdud,rddd],[ruuuu,ruuud,rudud,ruddd,rdddd]]

finalRate2 = [list(reversed(x)) for x in finalRate]

print_lattice2(finalRate2, info = [])

"""
                 0                   1                   2                   3                   4
------------------|-------------------|-------------------|-------------------|-------------------
                                                                                0.2800765880912329
                                                            0.2284042449051832  0.2033773447493335
                                        0.1969412402569137  0.1625713631165124  0.1476822630523326
                    0.1431804665295065  0.1374012409543158  0.1157134715973974  0.1072393331083148
0.1000000000000000  0.0979155956125509  0.0958615929866076  0.0823614150268616  0.0778717384730276


"""
