from scipy.optimize import fsolve
import math
from scipy.stats import norm

"""

Source: Distance to Default (According to KMV Model) by Tetereva Anastasija

Please read in conjuction with the article above (google it)

This is just a conceptual framework for the KMV Model not the real model.

"""

#Step 1 - Declare variables _Observable Parameters

s0 = 4740291.0
sigmaS = 0.02396918
r = 2.32
T = 1 
B = 33404048.0

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
    

estimatedParameters = fsolve(MertonSolve,[0.02396919,4740291])


#What are the Estimated Values
sigmaV = estimatedParameters[0]
v0 = estimatedParameters[1]


print

print "v0 and sigmaV are " + str(v0), str(sigmaV)
print
#8023026.57048 0.0141618482951



#Compute Distance to Default (DD) explicitly
DD = (math.log(v0/B) + (r + sigmaV**2/2.0)*T)/(sigmaV*math.sqrt(T))
#d2 = d1 - sigmaV * math.sqrt(T)

print "DD are " + str(DD)
print

#63.1089176115




print "The Probability of Default is " + str(round(norm.cdf(-DD),5))
#The Probability of Default is 0.0




    
    
    
    
