'''Using the Secant method and Net Present Value (NPV) to Iteratively
   generate the Internal Rate of Return (IRR)
   To read more about the Secant method with Net Prsent Value for calculating
   IRR - Please visit - http://tinyurl.com/mszpvnh .
   This method also used Bisection Search to do the iteration - You can read about
   it on Wikipedia'''


#Net Present Value (NPV)
#Example Call - npv(0.5,[-100,60,60,60])

def npv(r,cashflow):
    total = 0.0
    for x in range(0,len(cashflow), 1):
        total += cashflow[x]/(1+r)**x
    return total

    
        

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
    npv0 = npv(guess0, cashflow)
    npv1 = npv(guess1, cashflow)
    irr = guess1 -( npv1 * (guess1 - guess0)/(npv1-npv0))
    remainder = irr - guess1

    while abs(remainder) > epsilon:
        if remainder < 0:
            guess0 = guess1
            guess1 = irr
        else:
            guess1 = guess0
            guess0 = irr
            

        npv0 = npv(guess0, cashflow)
        npv1 = npv(guess1, cashflow)
        irr = guess1 - (npv1 * (guess1 - guess0)/(npv1-npv0))
        remainder = irr - guess1
    return irr

#Sample Calls to functions:
print""
print  "CALCULATION RESULTS:"
print('_'*20)
print""
print "Net Future Value: {0:.5f}".format(nfv(0.5,[-100,-60,-60,500,50,60,90,80,75,50,100,200])) 
print""
print "Net Present Value: {0:.5f}".format(npv(0.5,[-100,-60,-60,500,50,60,90,80,75,50,100,200]))
print""
print "Internal Rate of Return: {0:.5f}".format(irr([-100,-60,-60,500,50,60,90,80,75,50,100,200]))

