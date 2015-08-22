"""
Topic : Ho Lee Short Rate Model Prototype in Python.

Objective : Prototype Model for Constructing the Ho Lee Short Rate Model in Python.

To be converted to an article in the near future. The goal is to show a simplified method for building the HL
model in R or Python. This is a simple exam/program for illustration only

***In order to find it easier to understand though readers have to wait for the article with
illustrations of the trees and explanation of the program. This is just a working file.

Background: The primary source listed below is a research paper commissioned by the CFA Institute (formerly known as
AIMR) in 2001 to develop an easy framework for building/implementing short rate models in a computer program.
The goal of our code is to further simplify the approach discussed in the monograph by using numerical methods
and R so that the models can be understood by a wider audience because in their raw forms these models
require a high degree of mathematical sophistication. The five models discussed in the source which we will cover are
(a) Ho-Lee, (b) Kalotay-Fabozzi-Williams, (c) Black-Derman-Toy, (d) Black-Karasinski and (e) Hull-White.

Motivation: This is a personal research that attempts to simplify the short-rate models discussed in the primary
source further (lets hope we are successful in achieving this goal at the end of the day)

Primary Source: Term Structure Models Using Binomial Trees by the Research Foundation of the AIMR - Gerald Beutow and
James Sochacki

Secondary Source: Understanding CVA, DVA, and FVA: Examples of Interest Rate Swap Valuation by Don Smith
Other Secondary Sources will be listed later

Implementation and Calibration for the Binomial Models - Ho Lee Short Rate Model.

"""


#########################################################################
#
#Node 0    Node 1      Node 2      Node 3       Node 4       Node 5
#
#                                                            0.066643
#                                               0.0632758
#                                  0.0616506                 0.0616437
#                       0.056084                0.0582758
#            0.05263               0.0566506                 0.0566437
#0.04969                0.051084                0.0532758
#            0.04763               0.0516506                 0.0516437
#                       0.046084                0.0482758
#                                  0.0466506                 0.0466437
#                                               0.0432758
#                                                            0.04164375
#
##########################################################################

"""
To be used in a forthcoming article on valuation of bonds with embedded options (puts and calls) - code used to automatically 
generate the tree not released.  To be extended to other short rate models and will be used to discuss the foundations of bond
valuation before we segway to more current topics.  It is necessary to discuss these topics because they are germane to understanding
more advanced topics.  This model can be easily extended to KFW and BDT.  We will also discuss HW and BK.  The original model was 
prototyped a while back but this is an attempt to implement the model/program to automatically generate the tree with very 
minimal manual intervention. The tree or lattice can then be used to value option based bonds via backward induction. One Love!!!
---------------------------------
HO LEE SHORT RATE MODEL AUTOMATED
---------------------------------

                 0                   1                   2                   3                   4                   5
------------------|-------------------|-------------------|-------------------|-------------------|-------------------
                                                                                                    0.0666406658433981
                                                                                0.0632727301924193  0.0616406658433981
                                                            0.0616475327871895  0.0582727301924193  0.0566406658433981
                                        0.0560816551104655  0.0566475327871895  0.0532727301924193  0.0516406658433981
                    0.0476315551112824  0.0510816551104655  0.0516475327871895  0.0482727301924194  0.0466406658433981
0.0496900000000000  0.0526315551112824  0.0460816551104655  0.0466475327871895  0.0432727301924193  0.0416406658433982

"""




from scipy.optimize import fsolve
import math

m = 0.02  #Initial Guess

a2 = 100/(1+0.04991*0.25)**2
a3 = 100/(1+0.05030*0.25)**3
a4 = 100/(1+0.05126*0.25)**4
a5 = 100/(1+0.05166*0.25)**5
a6 = 100/(1+0.05207*0.25)**6


def HoLee(m):
    ru = (0.04969 + m*0.25  + 0.005*math.sqrt(0.25))
    rd = (0.04969 + m*0.25  - 0.005*math.sqrt(0.25))
    N1 = 100/(1+ru*0.25) #FV value of bond is 100 at maturity
    N2 = 100/(1+rd*0.25)
    return((0.5*N1 + 0.5*N2)/(1+0.04969*0.25) - a2)
    
mo = fsolve(HoLee,m)
print mo[0]

ru = (0.04969 + mo*0.25  + 0.005*math.sqrt(0.25))
rd = (0.04969 + mo*0.25  - 0.005*math.sqrt(0.25))

print([ru,rd])

m = 0.02

def HoLee2(m):
    ruu = (0.04969 + (mo[0] + m)*0.25  + 2 *0.005*math.sqrt(0.25))
    rud = (0.04969 + (mo[0] + m)*0.25) 
    rdd = (0.04969 + (mo[0] + m)*0.25  - 2*0.005*math.sqrt(0.25))
  
    N1 = 100/(1+ruu*0.25) 
    N2 = 100/(1+rud*0.25)
    N3 = 100/(1+rdd*0.25)
    ans1 = ((0.5*N1 + 0.5*N2))/(1 + ru[0]*0.25)
    ans2 = ((0.5*N2 + 0.5*N3))/(1 + rd[0]*0.25)
  
    return((0.5*ans1 + 0.5*ans2)/(1+0.04969*0.25) - a3)

m1 = fsolve(HoLee2,m)
print m1


ruu = (0.04969 + (mo[0] + m1[0])*0.25  + 2 *0.005*math.sqrt(0.25))
rud = (0.04969 + (mo[0] + m1[0])*0.25) 
rdd = (0.04969 + (mo[0] + m1[0])*0.25  - 2*0.005*math.sqrt(0.25))

print ([ruu,rud,rdd])

def HoLee3(m):
    ruuu = (0.04969 + (mo[0] + m1[0]+m)*0.25  + 3 * 0.005*math.sqrt(0.25))
    ruud = (0.04969 + (mo[0] + m1[0]+m)*0.25  + 1 * 0.005*math.sqrt(0.25))
    rdud = (0.04969 + (mo[0] + m1[0]+m)*0.25  - 1 * 0.005*math.sqrt(0.25))
    rddd = (0.04969 + (mo[0] + m1[0]+m)*0.25  - 3 * 0.005*math.sqrt(0.25))
  
    N1 = 100/(1+ruuu*0.25) 
    N2 = 100/(1+ruud*0.25)
    N3 = 100/(1+rdud*0.25)
    N4 = 100/(1+rddd*0.25)
    
    ans1 = ((0.5*N1 + 0.5*N2))/(1 + ruu*0.25)
    ans2 = ((0.5*N2 + 0.5*N3))/(1 + rud*0.25)
    ans3 = ((0.5*N3 + 0.5*N4))/(1 + rdd*0.25)
    
    fans1 = ((0.5*ans1 + 0.5*ans2))/(1 + ru*0.25)
    fans2 = ((0.5*ans2 + 0.5*ans3))/(1 + rd*0.25)
    
    return((0.5*fans1 + 0.5*fans2)/(1+0.04969*0.25) - a4)

m2 = fsolve(HoLee3,m)
print m2

ruuu = (0.04969 + (mo[0] + m1[0]+m2[0])*0.25  + 3 * 0.005*math.sqrt(0.25))
ruud = (0.04969 + (mo[0] + m1[0]+m2[0])*0.25  + 1 * 0.005*math.sqrt(0.25))
rdud = (0.04969 + (mo[0] + m1[0]+m2[0])*0.25  - 1 * 0.005*math.sqrt(0.25))
rddd = (0.04969 + (mo[0] + m1[0]+m2[0])*0.25  - 3 * 0.005*math.sqrt(0.25))

print ([ruuu,ruud,rdud,rddd])

def HoLee4(m):
    ruuuu = (0.04969 + (mo[0] + m1[0]+ m2[0] + m)*0.25 + 4 * 0.005*math.sqrt(0.25))
    ruuud = (0.04969 + (mo[0] + m1[0]+ m2[0] + m)*0.25  + 2 * 0.005*math.sqrt(0.25))
    rudud = (0.04969 + (mo[0] + m1[0]+ m2[0] + m)*0.25  - 0 * 0.005*math.sqrt(0.25))
    ruddd = (0.04969 + (mo[0] + m1[0]+ m2[0] + m)*0.25  - 2 * 0.005*math.sqrt(0.25))
    rdddd = (0.04969 + (mo[0] + m1[0]+ m2[0] + m)*0.25  - 4 * 0.005*math.sqrt(0.25))
  
    N1 = 100/(1+ruuuu*0.25) 
    N2 = 100/(1+ruuud*0.25)
    N3 = 100/(1+rudud*0.25)
    N4 = 100/(1+ruddd*0.25)
    N5 = 100/(1+rdddd*0.25)
    
    ans1 = ((0.5*N1 + 0.5*N2))/(1 + ruuu*0.25)
    ans2 = ((0.5*N2 + 0.5*N3))/(1 + ruud*0.25)
    ans3 = ((0.5*N3 + 0.5*N4))/(1 + rdud*0.25)
    ans4 = ((0.5*N4 + 0.5*N5))/(1 + rddd*0.25)
    
    fans1 = ((0.5*ans1 + 0.5*ans2))/(1 + ruu*0.25)
    fans2 = ((0.5*ans2 + 0.5*ans3))/(1 + rud*0.25)
    fans3 = ((0.5*ans3 + 0.5*ans4))/(1 + rdd*0.25)
    
    xans1 = ((0.5*fans1 + 0.5*fans2))/(1 + ru*0.25)
    xans2 = ((0.5*fans2 + 0.5*fans3))/(1 + rd*0.25)
    
    return((0.5*xans1 + 0.5*xans2)/(1+0.04969*0.25) - a5)

m3 = fsolve(HoLee4,m)
print m3

ruuuu = (0.04969 + (mo[0] + m1[0]+ m2[0] + m3[0])*0.25 + 4 * 0.005*math.sqrt(0.25))
ruuud = (0.04969 + (mo[0] + m1[0]+ m2[0] + m3[0])*0.25  + 2 * 0.005*math.sqrt(0.25))
rudud = (0.04969 + (mo[0] + m1[0]+ m2[0] + m3[0])*0.25  - 0 * 0.005*math.sqrt(0.25))
ruddd = (0.04969 + (mo[0] + m1[0]+ m2[0] + m3[0])*0.25  - 2 * 0.005*math.sqrt(0.25))
rdddd = (0.04969 + (mo[0] + m1[0]+ m2[0] + m3[0])*0.25  - 4 * 0.005*math.sqrt(0.25))


print([ruuuu,ruuud,rudud,ruddd,rdddd])


def HoLee5(m):
    ruuuuu = (0.04969 + (mo[0] + m1[0]+ m2[0] + m3[0] + m)*0.25 + 5 * 0.005*math.sqrt(0.25))
    ruuuud = (0.04969 + (mo[0] + m1[0]+ m2[0] + m3[0] + m)*0.25  + 3 * 0.005*math.sqrt(0.25))
    ruuudd = (0.04969 + (mo[0] + m1[0]+ m2[0] + m3[0] + m)*0.25  + 1 * 0.005*math.sqrt(0.25))
    ruuddd = (0.04969 + (mo[0] + m1[0]+ m2[0] + m3[0] + m)*0.25  - 1 * 0.005*math.sqrt(0.25))
    rudddd = (0.04969 + (mo[0] + m1[0]+ m2[0] + m3[0] + m)*0.25  - 3 * 0.005*math.sqrt(0.25))
    rddddd = (0.04969 + (mo[0] + m1[0]+ m2[0] + m3[0] + m)*0.25  - 5 * 0.005*math.sqrt(0.25))
  
    N1 = 100/(1+ruuuuu*0.25) 
    N2 = 100/(1+ruuuud*0.25)
    N3 = 100/(1+ruuudd*0.25)
    N4 = 100/(1+ruuddd*0.25)
    N5 = 100/(1+rudddd*0.25)
    N6 = 100/(1+rddddd*0.25)
    
    ans1 = ((0.5*N1 + 0.5*N2))/(1 + ruuuu*0.25)
    ans2 = ((0.5*N2 + 0.5*N3))/(1 + ruuud*0.25)
    ans3 = ((0.5*N3 + 0.5*N4))/(1 + rudud*0.25)
    ans4 = ((0.5*N4 + 0.5*N5))/(1 + ruddd*0.25)
    ans5 = ((0.5*N5 + 0.5*N6))/(1 + rdddd*0.25)
    
    fans1 = ((0.5*ans1 + 0.5*ans2))/(1 + ruuu*0.25)
    fans2 = ((0.5*ans2 + 0.5*ans3))/(1 + ruud*0.25)
    fans3 = ((0.5*ans3 + 0.5*ans4))/(1 + rdud*0.25)
    fans4 = ((0.5*ans4 + 0.5*ans5))/(1 + rddd*0.25)
    
    xans1 = ((0.5*fans1 + 0.5*fans2))/(1 + ruu*0.25)
    xans2 = ((0.5*fans2 + 0.5*fans3))/(1 + rud*0.25)
    xans3 = ((0.5*fans3 + 0.5*fans4))/(1 + rdd*0.25)
    
    yans1 = ((0.5*xans1 + 0.5*xans2))/(1 + ru*0.25)
    yans2 = ((0.5*xans2 + 0.5*xans3))/(1 + rd*0.25)
    
    return((0.5*yans1 + 0.5*yans2)/(1+0.04969*0.25) - a6)

m4 = fsolve(HoLee5,m)
print m4

ruuuuu = (0.04969 + (mo[0] + m1[0]+ m2[0] + m3[0] + m4[0])*0.25 + 5 * 0.005*math.sqrt(0.25))
ruuuud = (0.04969 + (mo[0] + m1[0]+ m2[0] + m3[0] + m4[0])*0.25  + 3 * 0.005*math.sqrt(0.25))
ruuudd = (0.04969 + (mo[0] + m1[0]+ m2[0] + m3[0] + m4[0])*0.25  + 1 * 0.005*math.sqrt(0.25))
ruuddd = (0.04969 + (mo[0] + m1[0]+ m2[0] + m3[0] + m4[0])*0.25  - 1 * 0.005*math.sqrt(0.25))
rudddd = (0.04969 + (mo[0] + m1[0]+ m2[0] + m3[0] + m4[0])*0.25  - 3 * 0.005*math.sqrt(0.25))
rddddd = (0.04969 + (mo[0] + m1[0]+ m2[0] + m3[0] + m4[0])*0.25  - 5 * 0.005*math.sqrt(0.25))


print([ruuuuu,ruuuud,ruuudd,ruuddd,rudddd,rddddd])
