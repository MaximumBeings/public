"""
This code can be used to estimate the yield of a bond given other information
such as the bond price, a guess(of the yield), time to maturity (in months) and coupon payment.
This is my first attempt at converting the pseudocode in the textbook - A Primer for the mathermatics of Finance.
It uses Newton-Raphson to try and estimate the yield.  Note that it is an estimate.  I still need to compare it to
the Yield function in MS Excel and Wolfram Alpha.  In fact I need to rewrite the code in an updated version but this is
a rough prototype.  

Example Usage: Coupon 3.375%, Time to Maturity: 5 years, Bond_Price = 100 1/32, Compounding is semi-annually.
So this information need to be presented like below to the results function.

increment([6,12,18,24,30,36,42,48,54,60],[1.6875,1.6875,1.6875,1.6875,1.6875,1.6875,1.6875,1.6875,1.6875,101.6875],xold,100.03125)

Note that 3.375/2 = 1.6875 which will be paid 9 times and on the tenth payment you add the face value 100 + 1.6875 to make 101.6875
the total number of months is 5 years and 12 = 60 so each payment is due in 6, 12,18 , 24 etc month's time.
Present the time and cashflows as vectors or list. Leave the parameter xold as is because the initial guess is set at 0.1 and the final
parameter is the bond_Price.

#Second version coming soon.  But this version works as intended just need to refine the code.

"""
import math


def increment(t_cash_flow,v_cash_flow,xold,bond_Price):
    incremental = 0.0
    incremental2 = 0.0
    
    
    for x in range(len(t_cash_flow)):
        incremental +=  v_cash_flow[x]*math.exp(-xold*(t_cash_flow[x]/12.0))
    
    for x in range(len(t_cash_flow)):
        incremental2 += (t_cash_flow[x]/12.0)*v_cash_flow[x]*math.exp(-xold*(t_cash_flow[x]/12.0))
    
    
    return (incremental - bond_Price)/incremental2
    
def result():
    xo = 0.1
    epsilon = 0.000000000000000000001
    maxIterationCount = 6000
    xold = xo - 1
    xnew = xo
    i = 0
    try:
        while (i < maxIterationCount):
            xnew = xold + increment([6,12,18,24,30,36,42,48,54,60],[1.6875,1.6875,1.6875,1.6875,1.6875,1.6875,1.6875,1.6875,1.6875,101.6875],xold,100.03125)
        
            if abs(xnew - xold) <= epsilon:
                return xnew
                break
        
            xold = xnew
            i += 1
            
    except (OverflowError,RuntimeError, TypeError, NameError):
        print""
        print "Error"

#Sample Call
print""
print "The Yield of the Bond is: " + str(round(result(),20))
