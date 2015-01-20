#Topic : Ho Lee Short Rate Model Prototype in R 

#Objective : Prototype Model for Constructing the Ho Lee Short Rate Model in R.
#To be converted to an article in the near future.  The goal is to show a simplified method for building the HL
#model in R or Python.  This is a simple exam/program for illustration only

#***In order to find it easier to understand though readers have to wait for the article with
#illustrations of the trees and explanation of the program.  This is just a working file.

#Background: The primary source listed below is a research paper commissioned by the CFA Institute (formerly known as 
#AIMR) in 2001 to develop an easy framework for building/implementing short rate models in a computer program. 
#The goal of our code is to further simplify the approach discussed in the monograph by using numerical methods 
#and R so that the models can be understood by a wider audience because in their raw forms these models
#require a high degree of mathematical sophistication.  The five models discussed in the source which we will cover are
#(a) Ho-Lee, (b) Kalotay-Fabozzi-Williams, (c) Black-Derman-Toy, (d) Black-Karasinski and (e) Hull-White.

#Motivation: This is a personal research that attempts to simplify the short-rate models discussed in the primary
#source further (lets hope we are successful in achieving this goal at the end of the day)

#Primary Source: Term Structure Models Using Binomial Trees by the Research Foundation of the AIMR - Gerald Beutow and 
#James Sochacki

#Secondary Source: Understanding CVA, DVA, and FVA: Examples of Interest Rate Swap Valuation by Don Smith
#Other Secondary Sources will be listed later


#Implementation and Calibration for the Binomial Models - Ho Lee Short Rate Model.
# Assume a semiannial periodicity  (Zero-Coupon Bonds):
# 
# r0 = R1 = 3.5 Percent
# R2 = 4.25 Percent
# R3 = 5.5 Percent
# Constant Short Rate Volatility of 5 Percent.

# #################################################################################
#     FINAL BINOMIAL FORWARD RATE TREE - POPULATED MANUALLY FROM CALCULATION BELOW
#
# Node 0        Node 1             Node 2      
# 
#                                                               
#                                                   
#                                  0.15275147                           
#               0.08599255                           
# 0.0350                           0.08204079                     
#               0.01528187                           
#                                  0.01133011                      
#                                                   
#                                                                  
###################################################################################

#FORMULA TO BE GENERALIZED BUT FOR A START ->

ru = ro + mo * o.5 + vol * sqrt(0.5)
rd = ro + mo * o.5 - vol * sqrt(0.5)
ruu = ro + (mo + m1)*0.5 + 2 * vol * sqrt(0.5)
rud = ro + (mo + m1)*0.5 
rdd = ro + (mo + m1)*0.5 - 2 * vol * sqrt(0.5)

#There is a generalization of this formula but this is just to aid in establishing
#a pattern.

# #################################################################################
#     BINOMIAL TREE STRUCTURE
#
# Node 0        Node 1             Node 2                                                                   
#                                                   
#                                  ruu                           
#               ru                           
# ro                               rud                     
#               rd                           
#                                  rdd                      
#                                                   
#                                                                  
###################################################################################


#Calculation of Prices in Period 1, Period 2 and Period 3
a1 = 100/(1+0.0350*0.5)**1
a2 = 100/(1+0.0425*0.5)**2
a3 = 100/(1+0.055*0.5)**3

m = 0.02  #Initial Guess

HoLee1 <- function(m)
{
  ru = (0.035 + m*0.5  + 0.05*sqrt(0.5))
  rd = (0.035 + m*0.5  - 0.05*sqrt(0.5))
  N1 = 100/(1+ru*0.5) #FV value of bond is 100 at maturity
  N2 = 100/(1+rd*0.5)
  return((0.5*N1 + 0.5*N2)/(1+0.035*0.5) - a2)
}

#Use a root finding algorithm in R to find the value of R

mo = uniroot(HoLee1,c(0,1),tol = 1e-20)$root
ru = 0.035 + mo*0.5  + 0.05*sqrt(0.5)
rd = 0.035 + mo*0.5  - 0.05*sqrt(0.5)

data = c(ru,rd)
print(data)
#0.08599255 0.01528187

HoLee2 <- function(m)
{
  ruu = (0.035 + (mo + m)*0.5  + 2 *0.05*sqrt(0.5))
  rud = (0.035 + (mo + m)*0.5) 
  rdd = (0.035 + (mo + m)*0.5  - 2*0.05*sqrt(0.5))
  
  N1 = 100/(1+ruu*0.5) 
  N2 = 100/(1+rud*0.5)
  N3 = 100/(1+rdd*0.5)
  ans1 = ((0.5*N1 + 0.5*N2))/(1 + ru*0.5)
  ans2 = ((0.5*N2 + 0.5*N3))/(1 + rd*0.5)
  
  return((0.5*ans1 + 0.5*ans2)/(1+0.035*0.5) - a3)
}

#Use a root finding algorithm in R to find the value of R
m1 = uniroot(HoLee2,c(-1,1),tol = 1e-20)$root

ruu = (0.035 + (mo + m1)*0.5  + 2 *0.05*sqrt(0.5))
rud = (0.035 + (mo + m1)*0.5) 
rdd = (0.035 + (mo + m1)*0.5  - 2*0.05*sqrt(0.5))

data = c(ruu,rud,rdd)
print(data)
#0.15275147 0.08204079 0.01133011
