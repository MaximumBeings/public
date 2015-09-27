"""
This is the version to match Beninga and exactly the same methodology like the one I created like 9 months ago.  Output 
generated rated here is different from the one in the original essay and the one by John Hull.  I wish Hull can update his
technical note to include the calculations at node 4...then that will give the verdict as to which one is right.  This implement
ation is the one you will find all over the web and in most textbooks.

I only used Beninga to match my answer but did not use it as a source. The true source for this implementation is
Binomial Tree by the CFA Institute.  

Sources:  A One-Factor Model of Interest Rates and Its Application to Treasury Bond and Options by Fischer Black, Emanuel Derman
and William Toy.
          Technical Note No 23 - Options, Futures and Other Derivatives, Ninth Edition - The Black, Derman and Toy Model
          Binomial Term Structure Models by Simon Benninga and Zvi Wiener ( I used it to compare the outputs only).
          Analytical Edge - Mitx via Edx
          Binomial Trees by CFA Institute
          Original Version Also Used Understanding CVA, DVA, and FVA: Examples of Interest Rate Swap Valuation by Donald Smith
          The Donald Smith article used KWF but KWF is very close to BDT.  KWF accepts coupon and par bonds as inputs this
          accepts yield and yield volatility. The are very close.
          Beninga to match answers (I am not familiar with mathematica) but the answers are exactly the same.
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

a1 = 100/(1+0.1)**1  
a2 = 100/(1+0.11)**2  
a3 = 100/(1+0.12)**3
a4 = 100/(1+0.125)**4
a5= 100/(1+0.13)**5


def bdtOne(guess):
    ru = guess * math.exp(2 * 0.19)
    rd = guess 
    N1 = (100)/(1+ru)
    N2 = (100)/(1+rd)
    return (0.5*((N1/(1+r[0])) + (N2/(1+r[0])))-a2)
    
g = fsolve(bdtOne,m)[0]

ru = g * math.exp(2 * vol[1])
rd = g




def bdtTwo2(x):

    ruu = x[0] * math.exp(4 * 0.18)
    rud = x[0] * math.exp(2 * 0.18)
    rdd = x[0]
    N1 = (100)/(1+ruu)
    N2 = (100)/(1+rud)
    N3 = (100)/(1+rdd)
    ans1 = (0.5*N1 + 0.5*N2)/(1+ru)
    ans2 = (0.5*N2 + 0.5*N3)/(1+rd)

    
    return ((0.5*ans1 + 0.5*ans2)/(1+r[0])-a3)

k = fsolve(bdtTwo2,0.1)


ruu = k[0] * math.exp(4 * 0.18)
rud = k[0] * math.exp(2 * 0.18)
rdd = k[0]



def bdtThree3(x):
    ruuu = x[0] * math.exp(6 * 0.17)
    ruud = x[0] * math.exp(4 * 0.17)
    rdud = x[0] * math.exp(2 * 0.17)
    rddd = x[0]
  
    N1 = 100/(1+ruuu) 
    N2 = 100/(1+ruud)
    N3 = 100/(1+rdud)
    N4 = 100/(1+rddd)
    
    ans1 = ((0.5*N1 + 0.5*N2))/(1 + ruu)
    ans2 = ((0.5*N2 + 0.5*N3))/(1 + rud)
    ans3 = ((0.5*N3 + 0.5*N4))/(1 + rdd)
    
    fans1 = ((0.5*ans1 + 0.5*ans2))/(1 + ru)
    fans2 = ((0.5*ans2 + 0.5*ans3))/(1 + rd)
    

    
    return ((0.5*fans1 + 0.5*fans2)/(1+r[0]) - a4)



g = fsolve(bdtThree3,0.1,xtol=1.49012e-20 )
#bdtThree3([ 0.08271889,  0.16859304])

ruuu = g[0] * math.exp(6 * 0.17)
ruud = g[0] * math.exp(4 * 0.17)
rdud = g[0] * math.exp(2 * 0.17)
rddd = g[0]


def bdtFour(x):
    ruuuu = x[0] * math.exp(8 * 0.16)
    ruuud = x[0]  * math.exp(6 * 0.16)
    rudud = x[0]  * math.exp(4 * 0.16)
    ruddd = x[0]  * math.exp(2 * 0.16)
    rdddd = x[0]  
  
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


    
    return ((0.5*xans1 + 0.5*xans2)/(1+r[0]) -a5 )




g = fsolve(bdtFour,0.1,xtol=1.49012e-20)


ruuuu = g[0] * math.exp(8 * 0.16)
ruuud = g[0] * math.exp(6 * 0.16)
rudud = g[0] * math.exp(4 * 0.16)
ruddd = g[0] * math.exp(2 * 0.16)
rdddd = g[0] 



finalRate = [[0.1],[ru,rd],[ruu,rud,rdd],[ruuu,ruud,rdud,rddd],[ruuuu,ruuud,rudud,ruddd,rdddd]]

finalRate2 = [list(reversed(x)) for x in finalRate]

print_lattice2(finalRate2, info = [])

"""
                 0                   1                   2                   3                   4
------------------|-------------------|-------------------|-------------------|-------------------
                                                                                0.2800765880912321
                                                            0.2284042449051828  0.2033773447493330
                                        0.1969412402569144  0.1625713631165121  0.1476822630523322
                    0.1431804665295065  0.1374012409543162  0.1157134715973972  0.1072393331083146
0.1000000000000000  0.0979155956125509  0.0958615929866079  0.0823614150268615  0.0778717384730274

"""

"""
This is the function to call the automated version of the BDT prototype that matches Benninga.  I will create another one
for the prototype that matches the HW version.  Helper functions not included so you have to wait for an article on the topic.
I have decided that I am just going to automate the two versions of the implementation.  Take what you want from it. 
"""

def solutionIterator(mo,nNodes,rate3,rate2):
    for x in range(1,nNodes):
        data = (x,rate3)
        mo.append(fsolve(valueCalculator2,m,args=data)[0])
        #print mo
        rate2.append(rateCalculator2(mo[x],x))
        rate3 = rate2[1:]
        data = (x,rate3)
    return rate2
    
rate4 = solutionIterator(mo,nNodes,rate3,rate2)[:]




reversed_lists = [list(reversed(x)) for x in rate4]

#reversed_lists[1].reverse()

print "     "

print "---------------------------------------------------"
print "BLACK-DERMAN-TOY SHORT RATE MODEL AUTOMATED - VERSION THAT MATCHES BENNINGA"
print "---------------------------------------------------"

print_lattice2(reversed_lists, info = [])

print "     "


"""
---------------------------------------------------
BLACK-DERMAN-TOY SHORT RATE MODEL AUTOMATED - VERSION THAT MATCHES BENNINGA
---------------------------------------------------

                 0                   1                   2                   3                   4
------------------|-------------------|-------------------|-------------------|-------------------
                                                                                0.2800765880912328
                                                            0.2284042449051828  0.2033773447493335
                                        0.1969412402569142  0.1625713631165121  0.1476822630523326
                    0.1431804665295063  0.1374012409543162  0.1157134715973972  0.1072393331083148
0.1000000000000000  0.0979155956125507  0.0958615929866078  0.0823614150268615  0.0778717384730276

"""
