'''Another Newton-Raphson implementation.  I found this algorithm on the internet
written in Java and I converted it to Python.  Python is a cleaner language if performance is
not an issue.'''
import math

def irr(cashflow,guess=0.1):
    """
    >>>irr([-20000, -7000,5000,8000,9000])
    >>>-0.06736035818677397
    """
    epsilon = 0.00000000001
    maxIterationCount = 60
    x0 = guess
    x1 = 0.0
    i = 0
    try:
        while (i < maxIterationCount):
            fValue = 0
            fDerivative = 0;
            for k in range(len(cashflow)):
                fValue += cashflow[k]/math.pow(1.0+x0,k)
                fDerivative += -k * cashflow[k]/math.pow(1.0+x0,k+1);
            x1 = x0 - fValue/fDerivative
        
            if abs(x1 - x0) <= epsilon:
                return x1
        
            x0 = x1
            ++i
    except (OverflowError,RuntimeError, TypeError, NameError):
        print""
        print "Oops! I encountered an error and I cannot calculate the IRR for this cashflow stream."
        print""
        print "I will be updated in the future to address these types of cashflow streams."

#Example Call to Function
#irr([-20000, -7000,5000,8000,9000])
            
        
        
            
        