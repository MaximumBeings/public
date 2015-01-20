#Topic : Kalotay-Fabozzi-William  Short Rate Model Prototype in R
#Objective : Prototype Model for Constructing the Kalotay-Fabozzi-William Model in R.
#To be converted to an article in the near future. The goal is to show a simplified method for building the KFW
#model in R or Python.

#***In order to find it easier to understand though readers have to wait for the article with
#illustrations of the trees and explanation of the program. This is just a working file.

#Background: The primary source listed below is a research paper commissioned by the CFA Institute (formerly known as
#AIMR) in 2001 to develop an easy framework for building/implementing short rate models in a computer program.
#The goal of our code is to further simplify the approach discussed in the monograph by using numerical methods
#and R so that the models can be understood by a wider audience because in their raw forms these models
#require a high degree of mathematical sophistication. The five models discussed in the source which we will cover are
#(a) Ho-Lee, (b) Kalotay-Fabozzi-Williams, (c) Black-Derman-Toy, (d) Black-Karasinski and (e) Hull-White.

#Motivation: This is a personal research that attempts to further simplify the short-rate models discussed in the primary
#source  (lets hope we are successful in achieving this goal at the end of the day)

#Primary Source: Term Structure Models Using Binomial Trees by the Research Foundation of the AIMR - Gerald Beutow and
#James Sochacki

#Secondary Source: Understanding CVA, DVA, and FVA: Examples of Interest Rate Swap Valuation by Don Smith
#Other Secondary Sources will be listed later


# ############################################################################## 
#     FINAL BINOMIAL FORWARD RATE TREE - POPULATED MANUALLY FROM CALCULATION BELOW
#
# Year 0        Year 1             Year 2                
# 
#                                                                  
#                                                   
#                                  0.08601184                               
#               0.05179723                           
# 0.035                            0.08013993                      
#               0.04826110                           
#                                  0.07466889                      
#                                                   
#                                                                  
#################################################################################


#Implemented using Numerical Methods (Uniroot for Finding roots in R).  Not the most elegant code



#Conclusion - Same results as those in referenced article
#Comments - It can be reproduced in Excel using Solver




r = 2.000/100    #Initial Guess for the forward rate 
vol = 0.2    #Assumed Constant Volatility 20%
factor = exp(2*vol*sqrt(1))  #Proportionality Factor

#Probability Weights at each node - Lets Assume we know these numbers - Simplifying Assumption
#We Start from 50/50 and work our way up the nodes.

a1 = 100/(1+0.0350*0.5)**1
a2 = 100/(1+0.0425*0.5)**2
a3 = 100/(1+0.055*0.5)**3


#STEPS - 
#Calculate the binomial forward rates in Year 1 
#We assume that the rate on the last node i.e. N2 in this case is r
#In order to maintain proportionality we assume that all rates one node up is scaled by the factor
#We also maintain the probability weights of 50/50 at every node
#Our goal is to find r such that the final value of the bond is 100.00 which is the par value
#Repeat for every node
m = 0.02
kalotayK <- function(m)
{
  ru = 0.035*(exp(m*0.5+0.05*sqrt(0.5)))
  rd = 0.035*(exp(m*0.5-0.05*sqrt(0.5)))
  N1 = 100/(1+ru*0.5)    #FV value of bond is 102 at maturity
  N2 = 100/(1+rd*0.5)
  ans = (0+(0.5*N1 + 0.5*N2))/(1+0.035*0.5)
  return(ans - a2)
  
}

#Use a root finding algorithm in R to find the value of R
mo = uniroot(kalotayK,c(-1,1),tol = 1e-20)$root 
ru = 0.035*(exp(mo*0.5+0.05*sqrt(0.5)))
rd = 0.035*(exp(mo*0.5-0.05*sqrt(0.5)))

data0 = c(ru,rd)
print(data0)


kalotayK2 <- function(m)
{
  ruu = 0.035*(exp((mo+m)*0.5+2*0.05*sqrt(0.5)))
  rud = 0.035*(exp((mo+m)*0.5+0*0.05*sqrt(0.5)))
  rdd = 0.035*(exp((mo+m)*0.5-2*0.05*sqrt(0.5)))
  
  N1 = 100/(1+ruu*0.5) 
  N2 = 100/(1+rud*0.5)
  N3 = 100/(1+rdd*0.5)
  ans1 = ((0.5*N1 + 0.5*N2))/(1 + ru*0.5)
  ans2 = ((0.5*N2 + 0.5*N3))/(1 + rd*0.5)
  
  return((0.5*ans1 + 0.5*ans2)/(1+0.035*0.5) - a3)
}

#Use a root finding algorithm in R to find the value of R
m1 = uniroot(kalotayK2,c(-1,1),tol = 1e-20)$root

ruu = 0.035*(exp((mo+m1)*0.5+2*0.05*sqrt(0.5)))
rud = 0.035*(exp((mo+m1)*0.5+0*0.05*sqrt(0.5)))
rdd = 0.035*(exp((mo+m1)*0.5-2*0.05*sqrt(0.5)))

data1 = c(ruu,rud,rdd)
print(data1)



