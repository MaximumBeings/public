"""
Topic: Prototype Model for Black Derman Toy in Python.  I did this before in R a long time ago but I decided to use the original
article by Messers B, D & T because I want the article to be true to the spirit and intent of the original essay.  However, the
original article only explained the tree building process up to node 2.  However, in order to really be sure your algorithm is
working okay you must be able to verify your tree up to node 3.  Based on my experience once you build the third node, you can
be sure that your model is working okay.  Now the only real chance you have to do that is via the article by John Hull below. This
is the only article I found online that explained the mechanism for building the third node.  A lot of the papers out there
assume constant volatility, this is very easy to build if you make that simplifying assumption.  However, in this one we did not
assume constant volatility but rather used optimization techniques to find two unknowns...the rate at the lowest node and a 
volatility that will match the observed one.  I will  expantiate further on this model this weekend because there are so many 
variations of the implementation but this one tries to strictly match the original essay via John Hull's article.  So the output matches up
to node 3 exactly and are different for nodes 4 and 5. I am very certain that the methodology implemented here is correct and 
difference could be due to optimization tool used.  I am still researching it but you can check Binomial Trees by Simon Benninga 
and Zvi Wiener....they also did not get exactly the same output like in the original essay. I will prove node by node why I 
think the output from this design is correct.  I used Scipy....Beninga used Mathematica. The output from this model matched 
exactly with John Hull and BDT essay..up to third node.  Overall it is very close to the output by Beninga on all the nodes. The
is understandable because the computer is using trial and error to find the answers....no true root like in an analytical formula.


Sources:  A One-Factor Model of Interest Rates and Its Application to Treasury Bond and Options by Fischer Black, Emanuel Derman
and William Toy.
          Technical Note No 23 - Options, Futures and Other Derivatives, Ninth Edition - The Black, Derman and Toy Model
          Binomial Term Structure Models by Simon Benninga and Zvi Wiener ( I used it to compare the outputs only).
          Analytical Edge - Mitx via Edx
          
          
Discussion:  You have to wait for the essay to get a clearer picture.  Once we automate this, we will start writing the essays 
in about 2-3 weeks.  See you next time!
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

    ruu = x[0] * math.exp(4 * x[1])
    rud = x[0] * math.exp(2 * x[1])
    rdd = x[0]
    N1 = (100)/(1+ruu)
    N2 = (100)/(1+rud)
    N3 = (100)/(1+rdd)
    ans1 = (0.5*N1 + 0.5*N2)/(1+ru)
    ans2 = (0.5*N2 + 0.5*N3)/(1+rd)
    
    yu = math.sqrt(100/ans1) - 1
    yd = math.sqrt(100/ans2) - 1

    out = [((0.5*ans1 + 0.5*ans2)/(1+r[0])-a3)]
    out.append((0.5 * math.log(yu/yd) - 0.18))
    
    return out

k = fsolve(bdtTwo2,[0.1,0.1])


ruu = k[0] * math.exp(4 * k[1])
rud = k[0] * math.exp(2 * k[1])
rdd = k[0]



def bdtThree3(x):
    ruuu = x[0] * math.exp(6 * x[1])
    ruud = x[0] * math.exp(4 * x[1])
    rdud = x[0] * math.exp(2 * x[1])
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
    
    
    yuu = math.sqrt(100/ans1) - 1
    yud = math.sqrt(100/ans2) - 1
    ydd = math.sqrt(100/ans3) - 1
    
    out = [((0.5*fans1 + 0.5*fans2)/(1+r[0]) - a4)]
    out.append((0.5 * math.log(yuu/yud) - 0.17 ))
    
    return out



g = fsolve(bdtThree3,[0.1,0.1],xtol=1.49012e-20 )
#bdtThree3([ 0.08271889,  0.16859304])

ruuu = g[0] * math.exp(6 * g[1])
ruud = g[0] * math.exp(4 * g[1])
rdud = g[0] * math.exp(2 * g[1])
rddd = g[0]


def bdtFour(x):
    ruuuu = x[0] * math.exp(8 * x[1] )
    ruuud = x[0]  * math.exp(6 * x[1])
    rudud = x[0]  * math.exp(4 * x[1])
    ruddd = x[0]  * math.exp(2 * x[1])
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
    
    yuuu = math.sqrt(100/ans1) - 1
    yuud = math.sqrt(100/ans2) - 1
    ydud = math.sqrt(100/ans3) - 1
    yddd = math.sqrt(100/ans4) - 1
    
    out = [((0.5*xans1 + 0.5*xans2)/(1+r[0]) -a5 )]
    out.append(((0.5 * math.log(yuuu/yuud) - 0.16)))
    
    return out




g = fsolve(bdtFour,[0.1,0.1],xtol=1.49012e-20)
#bdtFour([ 0.08048839,  0.15227017])

ruuuu = g[0] * math.exp(8 * g[1])
ruuud = g[0] * math.exp(6 * g[1])
rudud = g[0] * math.exp(4 * g[1])
ruddd = g[0] * math.exp(2 * g[1])
rdddd = g[0] 



#Lattice printer not included

finalRate = [[0.1],[ru,rd],[ruu,rud,rdd],[ruuu,ruud,rdud,rddd],[ruuuu,ruuud,rudud,ruddd,rdddd]]

finalRate2 = [list(reversed(x)) for x in finalRate]

print_lattice2(finalRate2, info = [])

"""
                 0                   1                   2                   3                   4
------------------|-------------------|-------------------|-------------------|-------------------
                                                                                0.2721284603666325
                                                            0.2274672322883248  0.2006844763737346
                                        0.1941872111538781  0.1623606524845528  0.1479972326420377
                    0.1431804665295065  0.1376686893497773  0.1158891380091001  0.1091423774548019
0.1000000000000000  0.0979155956125509  0.0975999805273839  0.0827188860291753  0.0804883871396316




"""
