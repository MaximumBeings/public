from scipy.optimize import fsolve
import math
from scipy.stats import norm

#Source: Credit Risk on edx by Crillo

"""
Parameters:
s0 = 3  #Equity at time 0 i.e. today
sigmaS = 0.8 #Instanteous volatility of equity
r = 0.05 # Risk-free rate in the market
T = 1 #Maturity
B = 10 #Face value of the debt obligation 

Unobserved Parameters
v0  #Initial value of v0
sigmaV = Initial value of sigmaV
"""

#Step 1 - Declare variables _Observable Parameters

s0 = 3.0
sigmaS = 0.8
r = 0.05 
T = 1 
B = 10.0

#Step 2 - Calculate unobserved parameters via numerical method
#Create a function to do so

def MertonSolve(x):
    sigmaV = x[0]
    v0 = x[1]
    d1 = (math.log(v0/B) + (r + sigmaV**2/2.0)*T)/(sigmaV*math.sqrt(T))
    d2 = d1 - sigmaV * math.sqrt(T)
    F = v0 * norm.cdf(d1) - B * math.exp(-r * T) * norm.cdf(d2) - s0
    G = norm.cdf(d1) * sigmaV * v0 - sigmaS * s0
    out = []
    out.append(F**2)
    out.append(G**2)
    
    return out
    

estimatedParameters = fsolve(MertonSolve,[0.5,13])


#What are the Estimated Values
sigmaV = estimatedParameters[0]
v0 = estimatedParameters[1]


print

print "v0 and sigmaV are " + str(v0), str(sigmaV)
print
#0.212304713423 12.3953871895


#Compute d1 and d2 explicitly
d1 = (math.log(v0/B) + (r + sigmaV**2/2.0)*T)/(sigmaV*math.sqrt(T))
d2 = d1 - sigmaV * math.sqrt(T)

print "d1 and d2 are " + str(d1), str(d2)
print

#1.35313036908 1.14082565565


#print round(norm.cdf(-d2),5)
print "The Probability of Default is " + str(round(norm.cdf(-d2),5))
#0.12697


"""
v0 and sigmaV are 12.3953871895 0.212304713423

d1 and d2 are 1.35313036908 1.14082565565

The Probability of Default is 0.12697

"""
    
    
    
    
