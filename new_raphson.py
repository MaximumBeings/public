"""
This program uses the Newton-Raphson method to calculate IRR.  However, it does not
work for certain cashflow streams.  It works for most cashflows and generates the same
result as MS Excel and Wolfram Alpha.  If it cannot calculate the IRR for a certain cashflow
stream, it will generate an error message.  This is motivated by the Introduction to Corporate Finance
class by Wharton via Coursera course I am taking.
"""

def f(r,cashflow):
    total = 0.0
    total2 = 0.0
    result = []
    tracker = []
    tracker2 = []
    count = 0
    for x in xrange(0,len(cashflow), 1):
        total +=  cashflow[x]/(1+r)**x
        tracker.append(x)
        count += 1
    result.append(total)
    
    tracker2 = tracker[1:]
    cashflow2=cashflow[1:]
    
    count = 0
    for x in xrange(0,len(cashflow2), 1):
        total2 += (-1.0*cashflow2[x]*tracker2[x])/(1+r)**(x+1)
        count += 1
    result.append(total2)
        
    return result

def irr(cashflow):
    epsilon = 0.00000000000001
    guess0 = 0.01
    
    foo = f(guess0,cashflow)
    ans = guess0 - (foo[0]/foo[1])
    remainder = guess0 - ans
    
    try:
        while abs(remainder) > epsilon:
            guess0 = ans
            foo = f(guess0,cashflow)
            ans = guess0 - (foo[0]/foo[1]) 
            remainder = guess0 - ans
        
        print""
        print"RESULTS:"
        print "Internal Rate of Return: {0:.5f}".format(ans)
    
    except (OverflowError,RuntimeError, TypeError, NameError):
        print""
        print "Oops! I encountered an error and I cannot calculate the IRR for this cashflow stream."
        print""
        print "I will be updated in the future to address these types of cashflow streams."

##Net Present Value (NPV)
#Example Call - npv(0.5,[-100,60,60,60])

def npv(r,cashflow):
    total = 0.0
    for x in range(0,len(cashflow), 1):
        total += cashflow[x]/(1+r)**x
    
    print""
    print"RESULTS :"
    print "Net Present Value: {0:.3f}".format(total)
        
    
