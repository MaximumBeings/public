'''Using the Secant method and Net future Value (NFV) to Iteratively
   generate the Internal Rate of Return (IRR)
   The NFV is simply the sum of compounded cash flows; it may also be seen 
   as difference of compounded benefits and compounded costs.
   To read more about the Secant method with Net Future Value for calculating
   IRR - Please visit - http://tinyurl.com/mszpvnh .
   This method also uses Bisection Search to do the iteration - You can read about
   it on Wikipedia.  It was developed to solve problem sets on the Wharton's Introduction 
   to Corporate Finance Course offered via Coursera.  In the future, I hope to develop codes
   to calculate IRR using other methods such as Newton Raphson etc'''


#Net Present Value (NPV)
#Example Call - npv(0.5,[-100,60,60,60])

def npv(r,cashflow):
    total = 0.0
    for x in range(0,len(cashflow), 1):
        total += cashflow[x]/(1+r)**x

    print "Net Present Value: {0:.4f}".format(total)
        

#Net Future Value Function
#Example Call - nfv(0.5,[-100,60,60,60])

def nfv(r,cashflow):
    total = 0.0
    count = len(cashflow)
 
        
    for x in cashflow:
        total += x*(1+r)**count
        count -= 1
    return total

#Secant Method Using Bisection Search Approach
#Example Call - irr([-100,60,60,60])

def irr(cashflow):
    epsilon = 0.00000000000001
    guess0 = 0.5
    guess1 = 1
    nfv0 = nfv(guess0, cashflow)
    nfv1 = nfv(guess1, cashflow)
    irr = guess1 - nfv1 * (guess1 - guess0)/(nfv1-nfv0)
    remainder = irr - guess1

    while abs(remainder) > epsilon:
        if remainder < 0:
            guess0 = guess1
            guess1 = irr
        else:
            guess1 = guess0
            guess0 = irr
            

        nfv0 = nfv(guess0, cashflow)
        nfv1 = nfv(guess1, cashflow)
        irr = guess1 - nfv1 * (guess1 - guess0)/(nfv1-nfv0)
        remainder = irr - guess1
    print "Internal Rate of Return: {0:.6f}".format(irr)

#Sample Calls to functions:
print""
print  "CALCULATION RESULTS:"
print('_'*20)
print""
print "Net Future Value: {0:.3f}".format(nfv(0.5,[-1000,60,60,60,789])) 
print""
npv(0.5,[-1000,60,60,60])
print""
irr([-1000,60,60,60])
