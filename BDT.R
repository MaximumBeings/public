
#Topic : Black-Derman-Toy Short Rate Model Prototype in R

#Objective : Prototype Model for Constructing the Black-Derman-Toy Model in R.
#To be converted to an article in the near future. The goal is to show a simplified method for building the BDT
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
#source (lets hope we are successful in achieving this goal at the end of the day)

#Primary Source: Term Structure Models Using Binomial Trees by the Research Foundation of the AIMR - Gerald Beutow and
#James Sochacki

#Secondary Source: Understanding CVA, DVA, and FVA: Examples of Interest Rate Swap Valuation by Don Smith
#Other Secondary Sources will be listed later



a1 = 100/(1+0.09)**1
a2 = 100/(1+0.045)**2
a3 = 100/(1+0.05)**3
a4 = 100/(1+0.105)**4
a5 = 100/(1+0.11)**5


bdt1 <- function(rd)
{
  ru = rd*exp(2*0.08)
  rd = rd
  
  N1 = 100/(1+ru)    #FV value of bond is 102 at maturity
  N2 = 100/(1+rd)
  ans = (0.5*N1 + 0.5*N2)/(1+0.04)
  return(ans - a2)
  
}

#Use a root finding algorithm in R to find the value of R
rd = uniroot(bdt1,c(-1,1),tol = 1e-20)$root 
ru = rd*exp(2*0.08)
rd = rd

# #Verification
# vol1 = log(ru/rd)*0.5
# vol1 = 0.08
# rd = 0.04604461
# ru = 0.05403386
# log(ru/rd)*0.5 = 0.08
# We are correct!!!!

data0 <- c(ru,rd)
print(data0)


bdt2 <- function(rdd)
{
  ruu = rdd*exp(4*0.10)
  rud = rdd*exp(2*0.10)
  rdd = rdd
  
  N1 = 100/(1+ruu)    #FV value of bond is 102 at maturity
  N2 = 100/(1+rud)
  N3 = 100/(1+rdd)
  ans1 = (0.5*N1 + 0.5*N2)/(1+ru)
  ans2 = (0.5*N2 + 0.5*N3)/(1+rd)
  
  fans1 = (0.5*ans1 + 0.5*ans2)/(1+0.04)
  return(fans1 - a3)
  
}

#Use a root finding algorithm in R to find the value of R
rdd = uniroot(bdt2,c(-1,1),tol = 1e-20)$root 

ruu = rdd*exp(4*0.10)
rud = rdd*exp(2*0.10)
rdd = rdd

data1 <- c(ruu,rud,rdd)
print(data1)

# #Verification
# vol2 = log(ruu/rud)*0.5 or log(rud/rdd)*0.5
# vol2 = 0.1
# ruu = 0.07275296
# rud = 0.05956509
# rdd = 0.04876777
# log(ruu/rud)*0.5 = 0.1
# log(rud/rdd)*0.5 = 0.1
# We are correct!!!!
