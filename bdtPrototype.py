"""
Topic: BDT Prototype in Python

Source: A One-Factor Model of Interest Rates and Its Application To Treasury Bond Options.

Discussion:  Only correct to the second node...need to fix one or two things
before I automate it.
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

vol =math.log(ru/rd)*0.5



def bdtTwo(guess):
    ruu = guess * math.exp(4 * vol)
    rud = guess * math.exp(2 * vol)
    rdd = guess
    N1 = (100)/(1+ruu)
    N2 = (100)/(1+rud)
    N3 = (100)/(1+rdd)
    ans1 = (0.5*N1 + 0.5*N2)/(1+ru)
    ans2 = (0.5*N2 + 0.5*N3)/(1+rd)
    
    return ((0.5*ans1 + 0.5*ans2)/(1+r[0])-a2)

g = fsolve(bdtTwo,m,xtol=1.49012e-08)[0]

g = 0.0976
ruu = g * math.exp(4 * vol)
rud = g * math.exp(2 * vol)
rdd = g



vol =math.log(ruu/rud)*0.5


def bdtThree(guess):
    ruuu = guess * math.exp(6 * vol)
    ruud = guess * math.exp(4 * vol)
    rdud = guess * math.exp(2 * vol)
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


ruuu = g * math.exp(6 * vol)
ruud = g * math.exp(4 * vol)
rdud = g * math.exp(2 * vol)
rddd = g


vol =math.log(rdud/rddd)*0.5

def bdtFour(guess):
    ruuuu = guess * math.exp(8 * vol)
    ruuud = guess * math.exp(6 * vol)
    rudud = guess * math.exp(4 * vol)
    ruddd = guess * math.exp(2 * vol)
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

ruuuu = g * math.exp(8 * vol)
ruuud = g * math.exp(6 * vol)
rudud = g * math.exp(4 * vol)
ruddd = g * math.exp(2 * vol)
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
                                                                                0.3127755382482753
                                                            0.2311312693676162  0.2138951203536187
                                        0.2086957591204895  0.1580617555827786  0.1462746184286721
                    0.1431804665295065  0.1427189759287803  0.1080923349154180  0.1000315666906314
0.1000000000000000  0.0979155956125509  0.0976000000000000  0.0739201764803117  0.0684077281627750



"""
