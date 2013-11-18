import math
def irr(cashflow):
    min1 = 0.01;
    max1 = 1.1;
    guess = 0.0
    epsilon = 0.0000000001
    npv=1.0
    while abs(npv) > epsilon:
        npv=0.0
        guess = (min1 + max1) /2
        for k in range(len(cashflow)):
            npv += cashflow[k]/math.pow(1.0+guess,k)
        if npv > 0:
            min1 = guess
        else:
            max1 = guess
    return guess 
    
    
    
